import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, Request, status
from app.services.detection_service import DetectionService
from app.utils.image_validator import validate_image
from app.models.species_db import all_classes, SNAKE_DB

logger  = logging.getLogger("snake_api.router")
router  = APIRouter()
svc     = DetectionService()


@router.post(
    "/detect",
    summary="Deteksi Ular dari Gambar",
    description="""
Upload foto ular → hasil klasifikasi lengkap.

**Aturan confidence:**
- ≥ 70% → tampilkan spesies, status berbisa, saran tindakan
- < 70% → "Tidak dapat dipastikan, tetap waspada"

**Format yang didukung:** JPG, PNG, WEBP (maks 10MB)
""",
)
async def detect(
    request: Request,
    file: UploadFile = File(..., description="Foto ular"),
):
    client_ip = request.client.host if request.client else "unknown"

    try:
        image_bytes = await file.read()
    except Exception:
        raise HTTPException(400, detail="Gagal membaca file upload")

    ok, err = validate_image(image_bytes, file.filename or "upload")
    if not ok:
        raise HTTPException(400, detail=err)

    try:
        return await svc.analyze(image_bytes, file.filename or "unknown", client_ip)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deteksi: {e}", exc_info=True)
        raise HTTPException(500, detail="Terjadi kesalahan internal. Coba lagi.")


@router.get("/species", summary="Daftar Spesies yang Didukung")
async def species_list():
    result = []
    for key, info in SNAKE_DB.items():
        result.append({
            "class"         : key,
            "common_name"   : info.common_name,
            "scientific_name": info.scientific_name,
            "is_venomous"   : info.is_venomous,
            "risk_level"    : info.risk_level.value,
        })
    return {"total": len(result), "species": result}


@router.get("/stats", summary="Statistik Prediksi Hari Ini")
async def stats():
    from app.services.prediction_logger import PredictionLogger
    return await PredictionLogger().today_stats()
