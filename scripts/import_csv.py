# scripts/import_csv.py
import csv
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Sample, Base

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "ingest" / "parsed_samples.csv"
DB_PATH = REPO_ROOT / "qc_log.db"

def load_samples():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    inserted = 0
    skipped = 0
    with Session() as db:
        for row in rows:
            sid = row["sample_id"].strip().upper()
            if db.query(Sample).filter_by(sample_id=sid).first():
                skipped += 1
                continue

            s = Sample(
                sample_id=sid,
                material=row["material"] or None,
                log_number=row["log_number"] or None,
                date_cast=parse_date(row.get("date_cast")),
                cast_by=row["cast_by"] or None,
                logged_by=row["logged_by"] or None,
                logged_date=parse_date(row.get("logged_date")) or datetime.utcnow(),
                num_samples=int(row["num_samples"]) if row["num_samples"] else None,
                job_number=row["job_number"] or None,
                job_name=row["job_name"] or None,
                sample_type=row["sample_type"] or None,
                mix_number=row["mix_number"] or None,
                early_break=row["early_break"] or None,
                other_break=row["other_break"] or None,
                break_7_day=row["break_7_day"] or None,
                break_28_day_1=row["break_28_day_1"] or None,
                break_28_day_2=row["break_28_day_2"] or None,
                break_28_day_3=row["break_28_day_3"] or None,
                task_c1_4x8=row["task_c1_4x8"] or None,
                task_c2_6x12=row["task_c2_6x12"] or None,
                task_c3_shot=row["task_c3_shot"] or None,
                task_c4_grout=row["task_c4_grout"] or None,
                task_c5_cores=row["task_c5_cores"] or None,
                task_c6_mortar=row["task_c6_mortar"] or None,
                po_number=row["po_number"] or None
            )
            db.add(s)
            inserted += 1

        db.commit()

    print(f"✅ Imported {inserted} new samples. Skipped {skipped} existing.")

def parse_date(val):
    if not val:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(val.strip(), fmt)
        except ValueError:
            continue
    return None

if __name__ == "__main__":
    load_samples()
