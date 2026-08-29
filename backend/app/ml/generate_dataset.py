import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import random


SOURCE_DIR = Path("dataset/clean")
OUTPUT_DIR = Path("dataset/generated")

TRAIN_DIR = OUTPUT_DIR / "train"
TEST_DIR = OUTPUT_DIR / "test"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

random.seed(42)
np.random.seed(42)


def load_image(path):
    image = cv2.imread(str(path))

    if image is None:
        return None

    return image


def save_image(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)


def add_blur(image):
    kernel = random.choice([5, 7, 9])
    return cv2.GaussianBlur(image, (kernel, kernel), 0)


def add_underexposure(image):
    factor = random.uniform(0.25, 0.55)
    result = image.astype(np.float32) * factor
    return np.clip(result, 0, 255).astype(np.uint8)


def add_overexposure(image):
    factor = random.uniform(1.5, 2.2)
    result = image.astype(np.float32) * factor
    return np.clip(result, 0, 255).astype(np.uint8)


def add_noise(image):
    sigma = random.uniform(15, 45)

    noise = np.random.normal(
        0,
        sigma,
        image.shape
    )

    result = image.astype(np.float32) + noise

    return np.clip(
        result,
        0,
        255
    ).astype(np.uint8)


def add_severe_degradation(image):
    result = image.copy()

    # Strong blur
    result = cv2.GaussianBlur(
        result,
        (11, 11),
        0
    )

    # Reduce brightness
    result = result.astype(np.float32) * 0.45

    result = np.clip(
        result,
        0,
        255
    ).astype(np.uint8)

    # Add strong noise
    noise = np.random.normal(
        0,
        35,
        result.shape
    )

    result = result.astype(np.float32) + noise

    return np.clip(
        result,
        0,
        255
    ).astype(np.uint8)


def generate_variants(image):
    return {
        "clean": image,
        "blur": add_blur(image),
        "underexposure": add_underexposure(image),
        "overexposure": add_overexposure(image),
        "noise": add_noise(image),
        "severe_degradation": add_severe_degradation(image)
    }


def main():

    SOURCE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    TRAIN_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    TEST_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    source_images = [
        p for p in SOURCE_DIR.rglob("*")
        if p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if len(source_images) < 5:
        print()
        print("ERROR: At least 5 clean images are required.")
        print()
        print("Put clean JPG/PNG/WebP images inside:")
        print("dataset/clean/")
        print()
        print(f"Currently found: {len(source_images)}")
        return

    random.shuffle(source_images)

    split_index = max(
        1,
        int(len(source_images) * 0.8)
    )

    train_sources = source_images[:split_index]
    test_sources = source_images[split_index:]

    if not test_sources:
        test_sources = train_sources[-1:]
        train_sources = train_sources[:-1]

    rows = []

    def process_sources(sources, split_name):

        output_root = (
            TRAIN_DIR
            if split_name == "train"
            else TEST_DIR
        )

        for source_path in sources:

            image = load_image(source_path)

            if image is None:
                print(
                    f"Skipping unreadable image: "
                    f"{source_path}"
                )
                continue

            variants = generate_variants(image)

            source_name = source_path.stem

            for label, variant in variants.items():

                filename = (
                    f"{source_name}_{label}.jpg"
                )

                output_path = (
                    output_root /
                    label /
                    filename
                )

                save_image(
                    output_path,
                    variant
                )

                rows.append({
                    "split": split_name,
                    "source_image": source_path.name,
                    "filename": str(output_path),
                    "label": label
                })

    process_sources(
        train_sources,
        "train"
    )

    process_sources(
        test_sources,
        "test"
    )

    metadata_path = (
        OUTPUT_DIR / "metadata.csv"
    )

    pd.DataFrame(rows).to_csv(
        metadata_path,
        index=False
    )

    print()
    print("=" * 60)
    print("SMARTVISION DATASET GENERATED")
    print("=" * 60)
    print(
        f"Source images : {len(source_images)}"
    )
    print(
        f"Training images: {len(train_sources)}"
    )
    print(
        f"Test images    : {len(test_sources)}"
    )
    print(
        f"Generated samples: {len(rows)}"
    )
    print(
        f"Metadata: {metadata_path}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
