# app/api/warehouse_api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.models.material import Material
from app.services.auth import get_current_user

router = APIRouter(prefix="/warehouse", tags=["Warehouse"])

# ✅ Просмотр всех материалов на складе (только для warehouse, hvac, manager)
@router.get("/materials")
def get_all_materials(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["warehouse", "hvac", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    return db.query(Material).all()


# ✅ Добавить новый материал (только для warehouse)
@router.post("/materials")
def add_material(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse staff can add materials.")

    material = Material(
        name=data.get("name"),
        brand=data.get("brand"),
        category=data.get("category"),
        specs=data.get("specs"),
        price_usd=data.get("price_usd"),
        price_mxn=data.get("price_mxn"),
        stock=data.get("stock"),
        photo_url=data.get("photo_url"),
        arrival_date=data.get("arrival_date"),
        status=data.get("status"),
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


# ✅ Получить материал по ID
@router.get("/materials/{material_id}")
def get_material_by_id(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["warehouse", "hvac", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied.")

    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")
    return material
