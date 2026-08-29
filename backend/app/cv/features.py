import cv2
import numpy as np
import math


def calculate_entropy(gray):
    histogram = cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    )

    histogram = histogram.ravel()
    histogram = histogram / (histogram.sum() + 1e-10)

    entropy = 0.0

    for probability in histogram:
        if probability > 0:
            entropy -= probability * math.log2(probability)

    return float(entropy)


def extract_features(image):
    if image is None:
        raise ValueError("Invalid image")

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    height, width = image.shape[:2]

    # Sharpness using Laplacian variance
    sharpness = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    # Brightness
    brightness = float(
        np.mean(gray)
    )

    # Contrast
    contrast = float(
        np.std(gray)
    )

    # Noise estimation
    blurred = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    noise = float(
        np.std(
            gray.astype(np.float32)
            - blurred.astype(np.float32)
        )
    )

    # Saturation
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    saturation = float(
        np.mean(hsv[:, :, 1]) / 255.0
    )

    # Entropy
    entropy = calculate_entropy(gray)

    # Edge density
    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_density = float(
        np.mean(edges > 0)
    )

    return {
        "width": int(width),
        "height": int(height),
        "sharpness": round(sharpness, 4),
        "brightness": round(brightness, 4),
        "contrast": round(contrast, 4),
        "noise": round(noise, 4),
        "saturation": round(saturation, 4),
        "entropy": round(entropy, 4),
        "edge_density": round(edge_density, 4)
    }