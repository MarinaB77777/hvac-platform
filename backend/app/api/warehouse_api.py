from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from app.schemas.user_schemas import User
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse"],
)

# 🔒 Проверка на роль склада
def verify_warehouse_role(user: User):
    if user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return user

# 📦 Получить все материалы склада
@router.get("/materials")
def get_all_materials(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    verify_warehouse_role(user)
    return db.query(Material).all()

# ➕ Добавить новый материал
@router.post("/materials")
def add_material(material: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    verify_warehouse_role(user)
    new_material = Material(**material)
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

# ✅ Принять материал на баланс
@router.post("/accept/{material_id}")
def accept_material(material_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    verify_warehouse_role(user)
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.stock = material.qty_received
    db.commit()
    return {"message": "Material accepted to stock"}
