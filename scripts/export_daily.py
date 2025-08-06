# scripts/export_daily.py
from datetime import datetime, timedelta
from pathlib import Path
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Sample, Base
from scripts.export_sheet import generate_pdf  # reuse existing ReportLab renderer

# Config
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "qc_log.db"
CSV_PATH = REPO_ROOT / "daily_sample_log.csv"
PDF_PATH = REPO_ROOT / "daily_sample_log.pdf"

def fetch_todays_samples():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    today = datetime(2025, 8, 1).date()
    tomorrow = today + timedelta(days=1)

    with Session() as db:
        return db.query(Sample).filter(
            Sample.created_at >= datetime.combine(today, datetime.min.time()),
            Sample.created_at < datetime.combine(tomorrow, datetime.min.time())
        ).order_by(Sample.sample_id).all()

def write_csv(samples):
    if not samples:
        print("⚠️ No samples found for today.")
        return

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sample_id", "material", "job_number", "job_name", "num_samples",
            "cast_by", "logged_by", "date_cast", "logged_date", "mix_number"
        ])
        for s in samples:
            writer.writerow([
                s.sample_id, s.material, s.job_number, s.job_name, s.num_samples,
                s.cast_by, s.logged_by,
                s.date_cast.isoformat() if s.date_cast else "",
                s.logged_date.isoformat() if s.logged_date else "",
                s.mix_number
            ])
    print(f"✅ Wrote {len(samples)} to CSV → {CSV_PATH}")

def main():
    samples = fetch_todays_samples()
    write_csv(samples)
    generate_pdf()  # same layout as full sheet
    print(f"✅ PDF also written to {PDF_PATH}")

if __name__ == "__main__":
    main()
