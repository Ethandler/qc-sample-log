from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models import Base, Sample
from scripts.export_sheet import generate_pdf
from scripts.import_csv import load_samples as import_from_csv
from pathlib import Path
import csv

# --- Setup
app = FastAPI(title="QC Sample Log API")
engine = create_engine("sqlite:///qc_log.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# --- API Endpoints
@app.get("/samples")
def list_samples():
    with SessionLocal() as db:
        samples = db.query(Sample).order_by(Sample.sample_id).all()
        return [s.sample_id for s in samples]

@app.post("/import_csv")
def import_csv():
    try:
        import_from_csv()
        return {"status": "imported"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/export_csv")
def export_csv():
    from scripts.export_daily import fetch_todays_samples
    samples = fetch_todays_samples()
    if not samples:
        return {"message": "No samples today"}
    
    CSV_PATH = Path("daily_sample_log.csv")
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "material", "job_number", "job_name"])
        for s in samples:
            writer.writerow([s.sample_id, s.material, s.job_number, s.job_name])
    return FileResponse(CSV_PATH)

@app.get("/export_pdf")
def export_pdf():
    generate_pdf()
    return FileResponse("daily_sample_log.pdf")

# --- Serve React Frontend
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = frontend_dist / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"error": "index.html not found"}
