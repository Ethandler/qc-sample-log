# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Counter(Base):
    __tablename__ = "counters"
    id = Column(Integer, primary_key=True)
    material = Column(String, unique=True, nullable=False)
    prefix = Column(String, nullable=False)
    current = Column(Integer, nullable=False)

class Sample(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True)
    sample_id = Column(String, unique=True, nullable=False)
    material = Column(String, nullable=False)
