from fastapi import APIRouter, HTTPException
from sqlalchemy import func

from app.database.database import SessionLocal
from app.models.image_analysis import ImageAnalysis


router = APIRouter(
    prefix="/api",
    tags=["Analysis History"]
)


@router.get("/analyses")
def get_analyses():

    db = SessionLocal()

    try:

        records = (
            db.query(ImageAnalysis)
            .order_by(ImageAnalysis.id.desc())
            .all()
        )

        return [
            {
                "id": record.id,
                "filename": record.filename,
                "content_type": record.content_type,
                "prediction": record.prediction,
                "confidence": record.confidence,

                "features": {
                    "width": record.width,
                    "height": record.height,
                    "sharpness": record.sharpness,
                    "brightness": record.brightness,
                    "contrast": record.contrast,
                    "noise": record.noise,
                    "saturation": record.saturation,
                    "entropy": record.entropy,
                    "edge_density": record.edge_density
                }
            }
            for record in records
        ]

    finally:

        db.close()


@router.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int):

    db = SessionLocal()

    try:

        record = (
            db.query(ImageAnalysis)
            .filter(ImageAnalysis.id == analysis_id)
            .first()
        )

        if record is None:

            raise HTTPException(
                status_code=404,
                detail="Analysis not found"
            )

        return {
            "id": record.id,
            "filename": record.filename,
            "content_type": record.content_type,
            "prediction": record.prediction,
            "confidence": record.confidence,

            "features": {
                "width": record.width,
                "height": record.height,
                "sharpness": record.sharpness,
                "brightness": record.brightness,
                "contrast": record.contrast,
                "noise": record.noise,
                "saturation": record.saturation,
                "entropy": record.entropy,
                "edge_density": record.edge_density
            }
        }

    finally:

        db.close()


@router.get("/dashboard")
def dashboard():

    db = SessionLocal()

    try:

        total = db.query(ImageAnalysis).count()

        overexposure = (
            db.query(ImageAnalysis)
            .filter(
                ImageAnalysis.prediction == "overexposure"
            )
            .count()
        )

        blur = (
            db.query(ImageAnalysis)
            .filter(
                ImageAnalysis.prediction == "blur"
            )
            .count()
        )

        clean = (
            db.query(ImageAnalysis)
            .filter(
                ImageAnalysis.prediction == "clean"
            )
            .count()
        )

        return {
            "total_analyses": total,
            "overexposure": overexposure,
            "blur": blur,
            "clean": clean
        }

    finally:

        db.close()