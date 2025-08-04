# app/allocator.py
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Counter, Sample

lock = threading.Lock()
engine = create_engine("sqlite:///qc_log.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

material_config = {
    "concrete":  ("C",    2300),
    "asphalt":   ("AC-",  184),
    "soil":      ("S",    1180),
    "masonry":   ("CMW-", 29)
}

Base.metadata.create_all(engine)

def reserve(material: str, qty: int = 1) -> list[str]:
    if material not in material_config:
        raise ValueError(f"Unsupported material: {material}")
    prefix, start = material_config[material]

    with lock:
        session = Session()
        counter = session.query(Counter).filter_by(material=material).first()
        if not counter:
            counter = Counter(material=material, prefix=prefix, current=start)
            session.add(counter)
            session.commit()

        ids = []
        for _ in range(qty):
            val = counter.current
            sample_id = f"{prefix}{val}"
            ids.append(sample_id)
            session.add(Sample(sample_id=sample_id, material=material))
            counter.current += 1

        session.commit()
        session.close()
        return ids
