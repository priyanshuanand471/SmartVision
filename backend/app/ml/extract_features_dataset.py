import sys
from pathlib import Path

# Add backend directory to Python path
BACKEND_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_DIR))

import cv2
import pandas as pd

from app.cv.features import extract_features


DATASET_DIR = Path("dataset/generated")
OUTPUT_FILE = DATASET_DIR / "features.csv"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def process_split(split):

    rows = []

    split_dir = DATASET_DIR / split

    if not split_dir.exists():
        return rows

    for label_dir in split_dir.iterdir():

        if not label_dir.is_dir():
            continue

        label = label_dir.name

        for image_path in label_dir.iterdir():

            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            image = cv2.imread(
                str(image_path)
            )

            if image is None:
                print(
                    f"Skipping: {image_path}"
                )
                continue

            try:

                features = extract_features(
                    image
                )

                row = {
                    "split": split,
                    "label": label,
                    "filename": str(
                        image_path
                    )
                }

                row.update(features)

                rows.append(row)

            except Exception as e:

                print(
                    f"Error processing "
                    f"{image_path}: {e}"
                )

    return rows


def main():

    print()
    print("=" * 60)
    print("SMARTVISION FEATURE EXTRACTION")
    print("=" * 60)

    train_rows = process_split("train")
    test_rows = process_split("test")

    rows = train_rows + test_rows

    if not rows:

        print("ERROR: No images found.")
        return

    df = pd.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Training samples : {len(train_rows)}"
    )

    print(
        f"Test samples     : {len(test_rows)}"
    )

    print(
        f"Total samples    : {len(rows)}"
    )

    print(
        f"Features         : {len(df.columns) - 3}"
    )

    print(
        f"Output           : {OUTPUT_FILE}"
    )

    print()
    print("FEATURE EXTRACTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
