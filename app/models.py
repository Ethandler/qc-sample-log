# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Counter(Base):
    __tablename__ = "counters"
    id       = Column(Integer, primary_key=True)
    material = Column(String, unique=True, nullable=False)
    prefix   = Column(String, nullable=False)
    current  = Column(Integer, nullable=False)

class Sample(Base):
    __tablename__ = "samples"
    id               = Column(Integer, primary_key=True)
    sample_id        = Column(String, unique=True, nullable=False)
    material         = Column(String, nullable=False)

    log_number       = Column(String)
    date_cast        = Column(DateTime)
    cast_by          = Column(String)
    logged_by        = Column(String)
    logged_date      = Column(DateTime)
    num_samples      = Column(Integer)
    job_number       = Column(String)
    job_name         = Column(String)
    sample_type      = Column(String)
    mix_number       = Column(String)

    early_break      = Column(String)
    other_break      = Column(String)
    break_7_day      = Column(String)
    break_28_day_1   = Column(String)
    break_28_day_2   = Column(String)
    break_28_day_3   = Column(String)

    task_c1_4x8      = Column(String)
    task_c2_6x12     = Column(String)
    task_c3_shot     = Column(String)
    task_c4_grout    = Column(String)
    task_c5_cores    = Column(String)
    task_c6_mortar   = Column(String)

    po_number        = Column(String)
    created_at       = Column(DateTime, default=datetime.utcnow, nullable=False)
