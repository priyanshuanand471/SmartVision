# SmartVision AI

SmartVision AI is an end-to-end image quality analysis
and defect detection system.

The system combines Computer Vision, Machine Learning,
REST APIs, database persistence, and a web-based dashboard.

---

## 1. Features

- Image upload
- JPEG / PNG / WebP validation
- File size validation
- Image integrity validation
- OpenCV image processing
- Automated image feature extraction
- Machine learning classification
- Prediction confidence
- Image quality scoring
- Quality issue detection
- Recommendations
- Analysis history
- Dashboard statistics
- REST API
- Automated API testing

---

## 2. Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- FastAPI
- Uvicorn

### Computer Vision

- OpenCV
- NumPy
- Pillow

### Machine Learning

- Scikit-learn
- Random Forest
- Joblib

### Database

- SQLite
- SQLAlchemy

### Testing

- Pytest
- HTTPX

---

## 3. Image Features

SmartVision extracts the following image features:

1. Width
2. Height
3. Sharpness
4. Brightness
5. Contrast
6. Noise
7. Saturation
8. Entropy
9. Edge Density

---

## 4. System Architecture

```text
                    USER
                      |
                      v
             FRONTEND APPLICATION
              HTML / CSS / JS
                      |
                      | HTTP
                      v
                  FASTAPI
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      Validation   OpenCV       Database
                      |
                      v
              Feature Extraction
                      |
                      v
                ML Prediction
                      |
                      v
             Quality Assessment
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Quality Report          SQLAlchemy / SQLite
          |
          v
       Frontend

## 5. ML Pipeline


Image
  |
  v
OpenCV
  |
  v
Feature Extraction
  |
  v
Feature Vector
  |
  v
Random Forest
  |
  v
Prediction
  |
  v
Confidence


## 6. Extracted Features


Sharpness

Laplacian variance is used to estimate image sharpness.

Brightness

Average grayscale intensity.

Contrast

Standard deviation of grayscale intensity.

Noise

Difference between original grayscale image
and Gaussian-blurred image.

Saturation

Average HSV saturation.

Entropy

Measures information content in the grayscale image.

Edge Density

Percentage of pixels detected as edges using Canny.


## 8. Example Analysis Response

{
    "id": 1,
    "filename": "sample.jpg",
    "prediction": "blur",
    "confidence": 0.91,
    "features": {
        "width": 3072,
        "height": 4096,
        "sharpness": 15.8099,
        "brightness": 126.6746,
        "contrast": 59.3018,
        "noise": 0.9488,
        "saturation": 0.2515,
        "entropy": 7.7801,
        "edge_density": 0.0061
    }
}




```
