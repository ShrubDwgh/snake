"""
Logging setiap prediksi ke file JSONL harian.
Format: 1 JSON object per baris — mudah di-parse untuk retraining.
"""

import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path

from app.config import settings

logger = logging.getLogger("snake_api.logger")


class PredictionLogger:
    _lock = asyncio.Lock()

    def __init__(self):
        self.log_dir = Path(settings.LOG_DIR)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _log_file(self, dt: datetime) -> Path:
        return self.log_dir / f"predictions_{dt.strftime('%Y-%m-%d')}.jsonl"

    def _anon_ip(self, ip: str) -> str:
        parts = ip.split(".")
        return f"{parts[0]}.{parts[1]}.x.x" if len(parts) == 4 else "unknown"

    async def log(self, prediction_id, filename, class_name, confidence,
                  venom_status, threshold_passed, top_predictions,
                  inference_time_ms, model_version, client_ip, processed_at):

        record = {
            "prediction_id"   : prediction_id,
            "processed_at"    : processed_at.isoformat(),
            "model_version"   : model_version,
            "filename"        : filename,
            "client_ip"       : self._anon_ip(client_ip),
            "predicted_class" : class_name,
            "confidence"      : confidence,
            "venom_status"    : venom_status,
            "threshold_passed": threshold_passed,
            "top_3"           : top_predictions,
            "inference_ms"    : inference_time_ms,
            # Untuk workflow retraining:
            "needs_review"    : not threshold_passed,
            "human_label"     : None,   # Diisi reviewer
        }

        async with self._lock:
            try:
                with open(self._log_file(processed_at), "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

                status_icon = "✅" if threshold_passed else "⚠️"
                logger.info(
                    f"[{prediction_id[:8]}] {class_name} | "
                    f"conf={confidence:.2%} | {status_icon} | {inference_time_ms}ms"
                )
            except Exception as e:
                logger.error(f"Log error: {e}")

    async def today_stats(self) -> dict:
        dt   = datetime.utcnow()
        path = self._log_file(dt)

        if not path.exists():
            return {"date": dt.strftime("%Y-%m-%d"), "total": 0}

        total = passed = venomous = uncertain = 0
        confs = []
        class_dist: dict[str, int] = {}

        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    total += 1
                    if r.get("threshold_passed"): passed += 1
                    if r.get("venom_status") == "BERBISA": venomous += 1
                    if r.get("venom_status") == "TIDAK DAPAT DIPASTIKAN": uncertain += 1
                    confs.append(r.get("confidence", 0))
                    cls = r.get("predicted_class", "unknown")
                    class_dist[cls] = class_dist.get(cls, 0) + 1
                except Exception:
                    continue

        return {
            "date"            : dt.strftime("%Y-%m-%d"),
            "total"           : total,
            "threshold_passed": passed,
            "threshold_failed": total - passed,
            "venomous_count"  : venomous,
            "uncertain_count" : uncertain,
            "avg_confidence"  : round(sum(confs) / len(confs), 4) if confs else 0,
            "needs_review"    : total - passed,
            "class_distribution": class_dist,
        }
