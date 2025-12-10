# app/schemas/material_request.py

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.schemas.material import MaterialOut  # если нужно возвращать подробности материала

class MaterialBaseInfo(BaseModel):
    id: int
    name: Optional[str]
    model: Optional[str]
    brand: Optional[str]
    organization: Optional[str] 

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
    issued_date: datetime
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    specs: Optional[str] = None
    price_usd: Optional[float] = None
    price_mxn: Optional[float] = None
    organization: Optional[str] = None

    class Config:
        from_attributes = True
