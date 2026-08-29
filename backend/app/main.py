from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router


app = FastAPI(
    title="SmartVision AI",
    description="AI-Powered Image Quality and Defect Detection System",
    version="1.0.0"
)


# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ======================================================
# ROUTERS
# ======================================================

app.include_router(
    analyze_router
)


# ======================================================
# HEALTH CHECK
# ======================================================

@app.get("/api/health")
def health_check():

    return {
        "status": "healthy",
        "service": "SmartVision AI"
    }