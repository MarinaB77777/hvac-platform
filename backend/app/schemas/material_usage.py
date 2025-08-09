# app/schemas/material_usage.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MaterialUsageBase(BaseModel):
    hvac_id: int
    order_id: int
    material_id: int
    quantity_used: int

    # копии свойств материала (в ответе нужны)
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    specs: Optional[str] = None
    price_usd: Optional[float] = None
    price_mxn: Optional[float] = None

class MaterialUsageCreate(MaterialUsageBase):
    pass

class MaterialUsageOut(MaterialUsageBase):
    id: int
    used_date: datetime  # <= важно: не used_at

    class Config:
        from_attributes = True
