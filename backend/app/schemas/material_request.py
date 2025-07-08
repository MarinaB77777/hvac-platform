# app/schemas/material_request.py

from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.material import MaterialOut  # если нужно возвращать подробности материала

class MaterialBaseInfo(BaseModel):
    id: int
    name: Optional[str]
    model: Optional[str]
    brand: Optional[str]

class MaterialRequestCreate(BaseModel):
    material_id: int
    quantity: int
    order_id: Optional[int] = None

class MaterialRequestOut(BaseModel):
    id: int
    material_id: int
    order_id: Optional[int]
    hvac_id: int
    quantity: int
    status: str
    material: Optional[MaterialOut]  # если включено relationship

    class Config:
        from_attributes = True
