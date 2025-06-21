# app/api/warehouse_api.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from typing import List
from pydantic import BaseModel
from datetime import date

router = APIRouter()


# 🔹 Pydantic-схема для вывода материалов
class MaterialOut(BaseModel):
    id: int
    name: str
    brand: str | None = None
    model: str | None = None
    material_type: str | None = None
    specs: str | None = None
    price_usd: float | None = None
    price_mxn: float | None = None
    stock: int
    photo_url: str | None = None
    arrival_date: date | None = None
    issued_date: date | None = None
    issued_to_hvac: int | None = None
    qty_issued: int | None = None
    status: str

    class Config:
        orm_mode = True


# 🔹 Получить все материалы со склада
@router.get("/materials", response_model=List[MaterialOut])
def get_all_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).all()
    return materials
