# 🐍 Snake Detection API — Siap Pakai

## Cara Menjalankan (3 langkah)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
> ⚠️ Proses ini butuh ~5-10 menit pertama kali karena download TensorFlow (~500MB).
> Setelah itu, jalankan berikutnya akan instan.

### 2. Jalankan server
```bash
python run.py
```
Tunggu sampai muncul: `✅ Model ready — API siap digunakan`

### 3. Buka browser
- **Test UI**: http://localhost:8000/static/index.html ← drag foto ular, langsung detect
- **Swagger Docs**: http://localhost:8000/docs ← dokumentasi interaktif
- **Stats hari ini**: http://localhost:8000/api/v1/stats

---

## Cara Pakai dari Kode

**Python:**
```python
import requests

with open("foto_ular.jpg", "rb") as f:
    res = requests.post(
        "http://localhost:8000/api/v1/detect",
        files={"file": f}
    )

data = res.json()
print(data["venom_status"])       # BERBISA / TIDAK BERBISA / TIDAK DAPAT DIPASTIKAN
print(data["confidence_pct"])     # 87.3%
print(data["species"]["common_name"])  # King Cobra
print(data["species"]["actions"])      # Daftar saran tindakan
```

**JavaScript (Web):**
```javascript
const form = new FormData();
form.append("file", fileInput.files[0]);

const res  = await fetch("http://localhost:8000/api/v1/detect", {
  method: "POST", body: form
});
const data = await res.json();

if (data.threshold_passed) {
  console.log(data.species.common_name);  // Nama ular
  console.log(data.venom_status);         // Status berbisa
} else {
  console.log("Tidak dapat dipastikan — confidence terlalu rendah");
}
```

**Android Kotlin (Retrofit):**
```kotlin
val file        = File(imagePath)
val requestFile = file.asRequestBody("image/jpeg".toMediaTypeOrNull())
val body        = MultipartBody.Part.createFormData("file", file.name, requestFile)

apiService.detectSnake(body).enqueue(object : Callback<JsonObject> {
    override fun onResponse(call: Call<JsonObject>, response: Response<JsonObject>) {
        val result = response.body()
        val status = result?.get("venom_status")?.asString
        val species = result?.getAsJsonObject("species")
    }
    override fun onFailure(call: Call<JsonObject>, t: Throwable) { }
})
```

---

## Struktur Response

```json
{
  "venom_status": "BERBISA",
  "confidence": 0.873,
  "confidence_pct": "87.3%",
  "threshold_passed": true,
  "message": "Terdeteksi: King Cobra (berbisa) dengan tingkat keyakinan 87.3%.",
  "warning": "🚨 Ular berbisa dengan risiko TINGGI!",
  "species": {
    "common_name": "King Cobra",
    "scientific_name": "Ophiophagus hannah",
    "description": "...",
    "risk_level": "TINGGI",
    "actions": ["Hubungi 119", "..."],
    "habitat": "Hutan hujan tropis",
    "distribution": "Sumatera, Jawa, Kalimantan",
    "fun_fact": "..."
  },
  "top_predictions": [...],
  "prediction_id": "abc123...",
  "processed_at": "2024-01-15T10:30:00",
  "inference_time_ms": 234.5,
  "model_version": "v1.0.0-mobilenetv2"
}
```

Kalau confidence < 70%:
```json
{
  "venom_status": "TIDAK DAPAT DIPASTIKAN",
  "threshold_passed": false,
  "species": null,
  "warning": "⚠️ Jangan abaikan ular yang tidak dikenali..."
}
```

---

## Log Prediksi (untuk Retraining)

Setiap prediksi otomatis disimpan di `logs/predictions_YYYY-MM-DD.jsonl`.

Baca statistik lewat API:
```
GET http://localhost:8000/api/v1/stats
```

Filter data yang perlu dilabel ulang:
```python
import json

with open("logs/predictions_2024-01-15.jsonl") as f:
    to_review = [json.loads(l) for l in f if json.loads(l)["needs_review"]]
```

---

## Catatan

Model yang dipakai sekarang adalah **MobileNetV2 + rule-based classifier** — sudah bisa berjalan
tapi akurasinya bergantung pada kualitas dan sudut foto. Untuk produksi, ganti fungsi
`_classify_features()` di `app/services/classifier.py` dengan model yang sudah ditraining
khusus dengan dataset ular Indonesia.
