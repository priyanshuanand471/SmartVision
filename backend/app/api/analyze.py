from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
import cv2
import numpy as np

from app.cv.features import extract_features
from app.ml.predict import predict_quality
from app.database.database import SessionLocal
from app.models.image_analysis import ImageAnalysis


router = APIRouter(
    prefix="/api",
    tags=["Image Analysis"]
)


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...)
):

    # -------------------------
    # 1. Validate file type
    # -------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="Unsupported image format. Use JPEG, PNG, or WebP."
        )

    # -------------------------
    # 2. Read file
    # -------------------------

    contents = await file.read()

    # -------------------------
    # 3. Validate file size
    # -------------------------

    max_size = 10 * 1024 * 1024

    if len(contents) > max_size:
        raise HTTPException(
            status_code=413,
            detail="Image size must be less than 10 MB."
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # -------------------------
    # 4. Validate image
    # -------------------------

    try:

        image = Image.open(
            io.BytesIO(contents)
        )

        image.verify()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid or unreadable image."
        )

    # -------------------------
    # 5. Convert bytes to OpenCV image
    # -------------------------

    try:

        image_array = np.frombuffer(
            contents,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:
            raise ValueError(
                "Unable to decode image"
            )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Unable to decode image."
        )

    # -------------------------
    # 6. Extract CV features
    # -------------------------

    try:

        features = extract_features(
            image
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to extract image features: {str(e)}"
        )

    # -------------------------
    # 7. ML Prediction
    # -------------------------

    try:

        prediction_result = predict_quality(
            features
        )

        prediction = prediction_result["prediction"]
        confidence = prediction_result["confidence"]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to predict image quality: {str(e)}"
        )

    # -------------------------
    # 8. Save result to database
    # -------------------------

    db = SessionLocal()

    try:

        analysis = ImageAnalysis(

            filename=file.filename,

            content_type=file.content_type,

            prediction=prediction,

            confidence=confidence,

            width=features["width"],

            height=features["height"],

            sharpness=features["sharpness"],

            brightness=features["brightness"],

            contrast=features["contrast"],

            noise=features["noise"],

            saturation=features["saturation"],

            entropy=features["entropy"],

            edge_density=features["edge_density"]
        )

        db.add(analysis)

        db.commit()

        db.refresh(analysis)

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to save analysis: {str(e)}"
        )

    finally:

        db.close()

    # -------------------------
    # 9. Return response
    # -------------------------

    return {

        "id": analysis.id,

        "filename": file.filename,

        "content_type": file.content_type,

        "status": "image_analyzed",

        "prediction": prediction,

        "confidence": confidence,

        "features": features
    }


# -------------------------
# GET all analysis history
# -------------------------

@router.get("/analyses")
def get_all_analyses():

    db = SessionLocal()

    try:

        analyses = (
            db.query(ImageAnalysis)
            .order_by(ImageAnalysis.id.desc())
            .all()
        )

        return [
            {
                "id": analysis.id,
                "filename": analysis.filename,
                "content_type": analysis.content_type,
                "prediction": analysis.prediction,
                "confidence": analysis.confidence,
                "features": {
                    "width": analysis.width,
                    "height": analysis.height,
                    "sharpness": analysis.sharpness,
                    "brightness": analysis.brightness,
                    "contrast": analysis.contrast,
                    "noise": analysis.noise,
                    "saturation": analysis.saturation,
                    "entropy": analysis.entropy,
                    "edge_density": analysis.edge_density
                }
            }
            for analysis in analyses
        ]

    finally:

        db.close()


# -------------------------
# GET single analysis
# -------------------------

@router.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int):

    db = SessionLocal()

    try:

        analysis = (
            db.query(ImageAnalysis)
            .filter(ImageAnalysis.id == analysis_id)
            .first()
        )

        if analysis is None:

            raise HTTPException(
                status_code=404,
                detail="Analysis not found."
            )

        return {
            "id": analysis.id,
            "filename": analysis.filename,
            "content_type": analysis.content_type,
            "prediction": analysis.prediction,
            "confidence": analysis.confidence,
            "features": {
                "width": analysis.width,
                "height": analysis.height,
                "sharpness": analysis.sharpness,
                "brightness": analysis.brightness,
                "contrast": analysis.contrast,
                "noise": analysis.noise,
                "saturation": analysis.saturation,
                "entropy": analysis.entropy,
                "edge_density": analysis.edge_density
            }
        }

    finally:

        db.close()