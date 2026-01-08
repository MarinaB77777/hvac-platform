# backend/app/api/materials.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.services.auth import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models.material import Material
from app.schemas.material import MaterialOut, MaterialCreate


router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("/", response_model=MaterialOut, status_code=201)
def create_material(
    material: MaterialCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # 🔒 только склад может добавлять материалы
    if current_user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can add materials")

    db_material = Material(
        **material.model_dump(),
        organization=current_user.organization  # ✅ КЛЮЧЕВО
    )

    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

from app.services.auth import get_current_user

@router.get("/", response_model=List[MaterialOut])
def get_all_materials(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    brand: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
):
    query = db.query(Material)

    # 🔐 ФИЛЬТР ПО ОРГАНИЗАЦИИ ДЛЯ СКЛАДА
    if current_user.role == "warehouse":
        if not current_user.organization:
            return []  # склад без организации ничего не видит
        query = query.filter(Material.organization == current_user.organization)


    if brand:
        query = query.filter(Material.brand == brand)

    if name:
        query = query.filter(Material.name.ilike(f"%{name}%"))


    if sort_by == "stock":
        query = query.order_by(Material.stock.desc())
    elif sort_by == "price":
        query = query.order_by(Material.price_usd.asc())

    return query.all()

@router.patch("/{material_id}/claim", response_model=MaterialOut)
def claim_material_to_my_org(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1) только склад
    if current_user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can claim materials")

    # 2) у складского пользователя должна быть организация
    if not current_user.organization:
        raise HTTPException(status_code=400, detail="Warehouse user has no organization")

    # 3) материал должен существовать
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # 4) если уже привязан — не трогаем
    if material.organization is not None and str(material.organization).strip() != "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Material already belongs to an organization",
        )

    # 5) забираем себе
    material.organization = current_user.organization

    db.add(material)
    db.commit()
    db.refresh(material)

    return material
