from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MaterialUsageCreate(BaseModel):
    material_id: int
    order_id: int
    quantity_used: int

class MaterialUsageOut(BaseModel):
    id: int
    hvac_id: int
    order_id: int
    material_id: int
    quantity_used: int
    used_at: datetime

    # 🔁 Подхватываем детали материала
    material_name: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    specs: Optional[str]

    class Config:
        from_attributes = True
