# backend/app/api/materials.py
# backend/app/api/materials.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models.material import Material
from app.schemas.material import MaterialOut, MaterialCreate

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("/", response_model=MaterialOut, status_code=201)
def create_material(
    material: MaterialCreate,
    db: Session = Depends(get_db)
):
    db_material = Material(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@router.get("/", response_model=List[MaterialOut])
def get_all_materials(
    db: Session = Depends(get_db),
    brand: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    organization: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None)
):
    query = db.query(Material)

    # 🔹 фильтр по бренду
    if brand:
        query = query.filter(Material.brand == brand)

    # 🔹 фильтр по названию
    if name:
        query = query.filter(Material.name.ilike(f"%{name}%"))

    # 🔥 фильтр по организации склада
    if organization:
        query = query.filter(Material.organization == organization)

    # 🔹 сортировка
    if sort_by == "stock":
        query = query.order_by(Material.stock.desc())
    elif sort_by == "price":
        query = query.order_by(Material.price_usd.asc())

    return query.all()
