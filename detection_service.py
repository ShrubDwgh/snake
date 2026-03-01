import uuid
import logging
from datetime import datetime

from app.services.classifier import SnakeClassifier
from app.services.prediction_logger import PredictionLogger
from app.models.species_db import get_species, RiskLevel

logger = logging.getLogger("snake_api.detection")


class DetectionService:
    def __init__(self):
        self.clf    = SnakeClassifier.get_instance()
        self.plogger = PredictionLogger()

    async def analyze(self, image_bytes: bytes, filename: str, client_ip: str) -> dict:
        pid  = str(uuid.uuid4())
        now  = datetime.utcnow()
        raw  = await self.clf.predict(image_bytes)

        class_name       = raw["class_name"]
        confidence       = raw["confidence"]
        is_venomous      = raw["is_venomous"]
        threshold_passed = raw["threshold_passed"]
        species          = get_species(class_name)

        # ── Threshold logic ────────────────────────────────────
        if not threshold_passed:
            venom_status = "TIDAK DAPAT DIPASTIKAN"
            message = (
                f"Gambar tidak dapat dikenali dengan cukup yakin "
                f"(confidence: {confidence:.1%}, minimal: 70%). "
                "Tetap waspada dan jauhi ular."
            )
            warning = (
                "⚠️ Jangan abaikan ular yang tidak dikenali. "
                "Hubungi BPBD (021-122) atau jauhi area tersebut."
            )
            species_data = None

        else:
            venom_status = "BERBISA" if is_venomous else "TIDAK BERBISA"
            sp_name = species.common_name if species else class_name.replace("_", " ").title()
            venom_label = "berbisa" if is_venomous else "tidak berbisa"
            message = (
                f"Terdeteksi: {sp_name} ({venom_label}) "
                f"dengan tingkat keyakinan {confidence:.1%}."
            )

            warning = None
            if is_venomous and species and species.risk_level == RiskLevel.HIGH:
                warning = (
                    "🚨 Ular berbisa dengan risiko TINGGI! "
                    "Segera hubungi 119 jika ada gigitan."
                )

            if species:
                species_data = {
                    "common_name"    : species.common_name,
                    "scientific_name": species.scientific_name,
                    "description"    : species.description,
                    "risk_level"     : species.risk_level.value,
                    "actions"        : species.actions,
                    "habitat"        : species.habitat,
                    "distribution"   : species.distribution,
                    "fun_fact"       : species.fun_fact,
                }
            else:
                species_data = None

        # ── Log prediksi ───────────────────────────────────────
        await self.plogger.log(
            prediction_id    = pid,
            filename         = filename,
            class_name       = class_name,
            confidence       = confidence,
            venom_status     = venom_status,
            threshold_passed = threshold_passed,
            top_predictions  = raw["top_predictions"],
            inference_time_ms= raw["inference_time_ms"],
            model_version    = raw["model_version"],
            client_ip        = client_ip,
            processed_at     = now,
        )

        return {
            "success"            : True,
            "venom_status"       : venom_status,
            "confidence"         : confidence,
            "confidence_pct"     : f"{confidence:.1%}",
            "threshold_passed"   : threshold_passed,
            "message"            : message,
            "warning"            : warning,
            "species"            : species_data,
            "top_predictions"    : raw["top_predictions"],
            "prediction_id"      : pid,
            "processed_at"       : now.isoformat(),
            "inference_time_ms"  : raw["inference_time_ms"],
            "model_version"      : raw["model_version"],
        }
