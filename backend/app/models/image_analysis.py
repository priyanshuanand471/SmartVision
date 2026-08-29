from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.database import Base


class ImageAnalysis(Base):

    __tablename__ = "image_analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    content_type = Column(
        String(100),
        nullable=False
    )

    prediction = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    width = Column(
        Integer
    )

    height = Column(
        Integer
    )

    sharpness = Column(
        Float
    )

    brightness = Column(
        Float
    )

    contrast = Column(
        Float
    )

    noise = Column(
        Float
    )

    saturation = Column(
        Float
    )

    entropy = Column(
        Float
    )

    edge_density = Column(
        Float
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )