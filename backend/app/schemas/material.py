from pydantic import BaseModel
from typing import Optional

class MaterialSchema(BaseModel):
    id: int
    name: str
    brand: Optional[str]
    model: Optional[str]
    material_type: Optional[str]
    specs: Optional[str]
    price_usd: Optional[float]
    price_mxn: Optional[float]
    stock: int
    photo_url: Optional[str]
    arrival_date: Optional[str]
    issued_date: Optional[str]
    issued_to_hvac: Optional[int]
    qty_issued: Optional[int]
    status: Optional[str]

    class Config:
        orm_mode = True
