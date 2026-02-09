from pydantic import BaseModel
from typing import Optional
from datetime import date

class PersonalMaterialCreate(BaseModel):
    name: str
    model: Optional[str] = None
    brand: Optional[str] = None
    specs: Optional[str] = None
    price_usd: Optional[float] = None
    price_mxn: Optional[float] = None
    stock: Optional[int] = 0
    photo_url: Optional[str] = None
    arrival_date: Optional[date] = None
    status: Optional[str] = None

class PersonalMaterialUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    specs: Optional[str] = None
    price_usd: Optional[float] = None
    price_mxn: Optional[float] = None
    stock: Optional[int] = None
    photo_url: Optional[str] = None
    arrival_date: Optional[date] = None
    status: Optional[str] = None

class PersonalMaterialOut(BaseModel):
    id: int
    name: str
    model: Optional[str] = None
    brand: Optional[str] = None
    specs: Optional[str] = None
    price_usd: Optional[float] = None
    price_mxn: Optional[float] = None
    stock: Optional[int] = None
    photo_url: Optional[str] = None
    arrival_date: Optional[date] = None
    status: Optional[str] = None
    organization: Optional[str] = None

    class Config:
        from_attributes = True
