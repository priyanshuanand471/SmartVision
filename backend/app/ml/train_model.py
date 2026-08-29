import joblib
import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)


DATASET_FILE = Path("dataset/generated/features.csv")
MODEL_DIR = Path("app/ml/models")

MODEL_FILE = MODEL_DIR / "smartvision_quality_model.joblib"


FEATURE_COLUMNS = [
    "width",
    "height",
    "sharpness",
    "brightness",
    "contrast",
    "noise",
    "saturation",
    "entropy",
    "edge_density"
]


def main():

    print()
    print("=" * 60)
    print("SMARTVISION ML MODEL TRAINING")
    print("=" * 60)

    if not DATASET_FILE.exists():

        print(
            f"ERROR: Dataset not found: "
            f"{DATASET_FILE}"
        )

        return

    df = pd.read_csv(
        DATASET_FILE
    )

    required_columns = (
        FEATURE_COLUMNS +
        ["split", "label"]
    )

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        print(
            "ERROR: Missing columns:"
        )

        print(missing)

        return

    train_df = df[
        df["split"] == "train"
    ].copy()

    test_df = df[
        df["split"] == "test"
    ].copy()

    X_train = train_df[
        FEATURE_COLUMNS
    ]

    y_train = train_df[
        "label"
    ]

    X_test = test_df[
        FEATURE_COLUMNS
    ]

    y_test = test_df[
        "label"
    ]

    print(
        f"Training samples : {len(X_train)}"
    )

    print(
        f"Test samples     : {len(X_test)}"
    )

    print()
    print("Training Random Forest...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print()
    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print()
    print("CLASSIFICATION REPORT")
    print("-" * 60)

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    labels = sorted(
        y_test.unique()
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=labels
    )

    print("CONFUSION MATRIX")
    print("-" * 60)

    print(
        "Labels:"
    )

    print(labels)

    print()

    print(matrix)

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    model_data = {
        "model": model,
        "features": FEATURE_COLUMNS,
        "labels": sorted(
            df["label"].unique()
        )
    }

    joblib.dump(
        model_data,
        MODEL_FILE
    )

    print()
    print("=" * 60)
    print("MODEL TRAINING COMPLETE")
    print("=" * 60)

    print(
        f"Model saved: {MODEL_FILE}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
