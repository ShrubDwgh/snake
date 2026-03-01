"""
Snake Detection API — Entry Point
Jalankan: uvicorn app.main:app --reload --port 8000
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import detection, health
from app.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("snake_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🐍 Snake Detection API starting...")

    from app.services.classifier import SnakeClassifier
    clf = SnakeClassifier.get_instance()
    await clf.load_model()
    logger.info("✅ Model ready — API siap digunakan")
    logger.info("📖 Docs: http://localhost:8000/docs")
    logger.info("🧪 Test UI: http://localhost:8000/static/index.html")

    yield

    logger.info("🛑 Shutting down...")


app = FastAPI(
    title="🐍 Snake Detection API",
    description=(
        "REST API deteksi ular berbisa berbasis AI. "
        "Upload foto ular → dapat hasil klasifikasi, info spesies, dan saran tindakan."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (halaman test UI)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(health.router,    prefix="/api/v1", tags=["Health"])
app.include_router(detection.router, prefix="/api/v1", tags=["Detection"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "name"   : "Snake Detection API",
        "version": "1.0.0",
        "docs"   : "/docs",
        "test_ui": "/static/index.html",
        "health" : "/api/v1/health",
    }
