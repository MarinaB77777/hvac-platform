from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MaterialUsageBase(BaseModel):
    hvac_id: int
    order_id: int
    material_id: int
    quantity_used: int

    # необязательные поля
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    specs: Optional[str] = None

class MaterialUsageCreate(MaterialUsageBase):
    pass

class MaterialUsageOut(MaterialUsageBase):
    id: int
    used_date: Optional[datetime] = None  
    
    class Config:
        from_attributes = True
