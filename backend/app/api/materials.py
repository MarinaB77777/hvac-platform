# app/api/materials.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.material import Material

router = APIRouter()


@router.get("/materials/")
def get_all_materials(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 🔒 Проверка роли пользователя
    if current_user.role not in ["warehouse", "hvac", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    materials = db.query(Material).all()
    return materials


@router.get("/materials/{material_id}")
def get_material_by_id(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["warehouse", "hvac", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    return material
