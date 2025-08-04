# app/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from .allocator import reserve

app = FastAPI()

class AllocationRequest(BaseModel):
    material: str
    qty: int = 1

@app.post("/reserve")
def reserve_ids(req: AllocationRequest):
    ids = reserve(req.material, req.qty)
    return {"ids": ids}
