# app/schemas/material.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class MaterialOut(BaseModel):
    id: int
    name: str
    model: Optional[str]
    brand: Optional[str]
    material_type: Optional[str]
    specs: Optional[str]
    price_usd: Optional[float]
    price_mxn: Optional[float]
    stock: int
    photo_url: Optional[str]
    arrival_date: Optional[date]
    issued_date: Optional[date]
    issued_to_hvac: Optional[int]
    qty_issued: Optional[int]
    status: Optional[str]

    model_config = {
        "from_attributes": True
    }
