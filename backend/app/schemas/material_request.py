# app/schemas/material_request.py

from pydantic import BaseModel
from typing import Optional


class MaterialRequestCreate(BaseModel):
    material_id: int
    order_id: Optional[int] = None
    quantity: int

class MaterialRequestOut(BaseModel):
    id: int
    material_id: int
    order_id: Optional[int] = None
    hvac_id: int
    quantity: int
    status: str

    class Config:
        orm_mode = True
