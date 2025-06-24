# backend/app/api/materials.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models.material import Material
from app.schemas.material import MaterialOut

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/", response_model=List[MaterialOut])
def get_all_materials(
    db: Session = Depends(get_db),
    material_type: Optional[str] = Query(None, description="Фильтр по типу материала"),
    brand: Optional[str] = Query(None, description="Фильтр по бренду"),
    name: Optional[str] = Query(None, description="Поиск по названию (включает подстроку)"),
    sort_by: Optional[str] = Query(None, description="Сортировка: 'stock' или 'price'")
):
    query = db.query(Material)

    if material_type:
        query = query.filter(Material.material_type == material_type)
    if brand:
        query = query.filter(Material.brand == brand)
    if name:
        query = query.filter(Material.name.ilike(f"%{name}%"))

    if sort_by == "stock":
        query = query.order_by(Material.stock.desc())
    elif sort_by == "price":
        query = query.order_by(Material.price_usd.asc())

    return query.all()
