# app/schemas/material_request.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class MaterialBaseInfo(BaseModel):
    id: int
    name: Optional[str]
    model: Optional[str]
    brand: Optional[str]

 class Config:
        from_attributes = True

class MaterialRequestOut(BaseModel):
    id: int
    material_id: int
    order_id: Optional[int]
    hvac_id: int
    quantity: int
    status: str
    material: Optional[MaterialBaseInfo]

class Config:
    from_attributes = True
