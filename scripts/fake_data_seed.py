# scripts/fake_data_seed.py
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Sample, Counter, Base

# Init DB
engine = create_engine("sqlite:///qc_log.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def ensure_counter(material, prefix, current):
    with Session() as db:
        counter = db.query(Counter).filter_by(material=material).first()
        if not counter:
            db.add(Counter(material=material, prefix=prefix, current=current))
            db.commit()

def create_sample(sid, material, dt, **kwargs):
    return Sample(
        sample_id=sid,
        material=material,
        created_at=dt,
        **kwargs
    )

def seed():
    ensure_counter("concrete", "C", 2284)
    ensure_counter("masonry", "CMW-", 29)
    ensure_counter("soil", "S", 1170)

    samples = []
    concrete_dates = [("2025-08-01", 8), ("2025-08-02", 12), ("2025-08-03", 10)]
    masonry_dates = [("2025-08-03", 4)]
    soil_dates = [("2025-08-04", 5)]

    sid = 2285
    for date_str, count in concrete_dates:
        base = datetime.strptime(date_str + " 06:30", "%Y-%m-%d %H:%M")
        for i in range(count):
            dt = base + timedelta(minutes=i * 7)
            samples.append(create_sample(
                f"C{sid}", "concrete", dt,
                log_number=str(sid),
                date_cast=dt,
                cast_by="Ethan",
                logged_by="Velahrin",
                logged_date=dt + timedelta(hours=1),
                num_samples=5,
                job_number="1588396",
                job_name="SR202–Val Vista–SR101",
                sample_type="Cylinder",
                mix_number="4000 PSI",
                break_7_day="08/08/25 - 3550 psi",
                break_28_day_1="08/29/25 - TBD",
                task_c1_4x8="✔",
                po_number="PO-0042"
            ))
            sid += 1

    mid = 30
    for date_str, count in masonry_dates:
        base = datetime.strptime(date_str + " 07:30", "%Y-%m-%d %H:%M")
        for i in range(count):
            dt = base + timedelta(minutes=i * 9)
            samples.append(create_sample(
                f"CMW-{mid}", "masonry", dt,
                job_number="G1234",
                sample_type="Grout",
                task_c4_grout="✔",
                date_cast=dt,
                logged_by="JCruz",
                logged_date=dt,
                po_number="PO-0031"
            ))
            mid += 1

    sid_soil = 1181
    for date_str, count in soil_dates:
        base = datetime.strptime(date_str + " 05:45", "%Y-%m-%d %H:%M")
        for i in range(count):
            dt = base + timedelta(minutes=i * 10)
            samples.append(create_sample(
                f"S{sid_soil}", "soil", dt,
                sample_type="Proctor",
                job_number="S9981",
                logged_by="ABurton",
                logged_date=dt
            ))
            sid_soil += 1

    with Session() as db:
        db.add_all(samples)
        db.commit()
        print(f"✅ Seeded {len(samples)} samples across concrete, masonry, soil.")

if __name__ == "__main__":
    seed()
