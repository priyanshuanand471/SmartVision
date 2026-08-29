def generate_quality_report(features, prediction):

    issues = []
    recommendations = []

    brightness = features["brightness"]
    sharpness = features["sharpness"]
    noise = features["noise"]
    contrast = features["contrast"]
    saturation = features["saturation"]
    edge_density = features["edge_density"]


    # Brightness
    if brightness > 220:

        issues.append("Image is too bright")
        recommendations.append(
            "Reduce camera exposure or lighting"
        )

    elif brightness < 40:

        issues.append("Image is too dark")
        recommendations.append(
            "Increase lighting or camera exposure"
        )


    # Sharpness
    if sharpness < 100:

        issues.append("Low image sharpness")
        recommendations.append(
            "Keep the camera stable and improve focus"
        )


    # Noise
    if noise > 10:

        issues.append("High image noise")
        recommendations.append(
            "Improve lighting or reduce camera ISO"
        )


    # Contrast
    if contrast < 25:

        issues.append("Low contrast")
        recommendations.append(
            "Improve lighting conditions"
        )


    # Saturation
    if saturation < 0.05:

        issues.append("Very low saturation")
        recommendations.append(
            "Check lighting and camera color settings"
        )


    # Edge density
    if edge_density < 0.01:

        issues.append("Low structural detail")
        recommendations.append(
            "Capture the object closer and in focus"
        )


    if not issues:

        issues.append("No major image quality issues detected")


    # Quality score

    score = 100


    if brightness > 220 or brightness < 40:
        score -= 20

    if sharpness < 100:
        score -= 20

    if noise > 10:
        score -= 15

    if contrast < 25:
        score -= 15

    if saturation < 0.05:
        score -= 10

    if edge_density < 0.01:
        score -= 10


    score = max(0, score)


    if score >= 80:

        quality = "GOOD"

    elif score >= 60:

        quality = "FAIR"

    else:

        quality = "POOR"


    return {
        "quality_score": score,
        "quality": quality,
        "prediction": prediction,
        "issues": issues,
        "recommendations": recommendations
    }