"""
Cara paling simpel jalankan API:
    python run.py

Atau manual:
    uvicorn app.main:app --reload --port 8000
"""
import subprocess
import sys

if __name__ == "__main__":
    print("🐍 Snake Detection API — Starting...")
    print("📖 Swagger docs : http://localhost:8000/docs")
    print("🧪 Test UI      : http://localhost:8000/static/index.html")
    print("📊 Stats        : http://localhost:8000/api/v1/stats")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
    ])
