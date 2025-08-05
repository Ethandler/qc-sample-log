# scripts/bootstrap_db.py
from sqlalchemy import create_engine
from app.models import Base

engine = create_engine("sqlite:///qc_log.db")
Base.metadata.create_all(engine)
print("✅ qc_log.db initialized with all tables.")
