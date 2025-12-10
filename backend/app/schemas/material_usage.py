# app/schemas/material_usage.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MaterialUsageBase(BaseModel):
    hvac_id: int
    order_id: int
    material_id: int
    quantity_used: int
    # копии свойств материала (как в модели SQLAlchemy)
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    specs: Optional[str] = None
    price_usd: Optional[float] = None
    price_mxn: Optional[float] = None
    organization: Optional[str] = None

class MaterialUsageCreate(MaterialUsageBase):
    # ничего не добавляем, фронту не нужно слать дату
    pass

class MaterialUsageOut(MaterialUsageBase):
    id: int
    used_at: datetime = Field(alias="used_date")  # ← ключевая строка

    class Config:
        from_attributes = True
        populate_by_name = True
