# scripts/time_loss_report.py
from pathlib import Path
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Sample

# Config
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "qc_log.db"
REPORT_CSV = REPO_ROOT / "time_loss_report.csv"

# Assumptions (tweak as needed)
GHOST_RATE = 0.02              # 2% of samples go unlogged, lost, or faked
COST_PER_GHOST = 75.0          # admin time, delays, compliance risk

def start_of_week(dt):
    return dt - timedelta(days=dt.weekday())

def fetch_samples():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Sample).all()

def group_samples_by_week(samples):
    weekly_counts = defaultdict(int)
    for s in samples:
        ts = getattr(s, "created_at", None)
        if ts:
            week = start_of_week(ts).date()
            weekly_counts[week] += 1
    return weekly_counts

def generate_report():
    samples = fetch_samples()
    weekly_counts = group_samples_by_week(samples)

    rows = []
    for week_start, count in sorted(weekly_counts.items()):
        ghost_est = round(count * GHOST_RATE)
        ghost_cost = round(ghost_est * COST_PER_GHOST, 2)
        week_end = week_start + timedelta(days=6)
        rows.append({
            "week_start": str(week_start),
            "week_end": str(week_end),
            "samples_logged": count,
            "ghost_samples_avoided": ghost_est,
            "dollars_saved_by_logging": ghost_cost
        })

    if not rows:
        print("⚠️ No samples found. No report written.")
        return

    with open(REPORT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Risk-based savings report written to: {REPORT_CSV}")
if __name__ == "__main__":
    generate_report()
