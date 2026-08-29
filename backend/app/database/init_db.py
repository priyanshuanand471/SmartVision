from app.database.database import Base, engine
from app.models.image_analysis import ImageAnalysis


def init_database():
    Base.metadata.create_all(
        bind=engine
    )

    print("DATABASE INITIALIZED SUCCESSFULLY")


if __name__ == "__main__":
    init_database()