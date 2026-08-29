import joblib
import pandas as pd
from pathlib import Path


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "smartvision_quality_model.joblib"
)


_model_data = None


def load_model():

    global _model_data

    if _model_data is None:

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}"
            )

        _model_data = joblib.load(
            MODEL_PATH
        )

    return _model_data


def predict_quality(features):

    model_data = load_model()

    model = model_data["model"]
    feature_columns = model_data["features"]

    values = [
        features[column]
        for column in feature_columns
    ]

    input_data = pd.DataFrame(
        [values],
        columns=feature_columns
    )

    prediction = model.predict(
        input_data
    )[0]

    probabilities = model.predict_proba(
        input_data
    )[0]

    confidence = float(
        max(probabilities)
    )

    return {
        "prediction": str(prediction),
        "confidence": round(
            confidence,
            4
        )
    }