from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.models.material_usage import MaterialUsage
from app.services.user_service import update_user
from app.schemas.user import UserUpdate
from app.services.auth import get_current_user

# ✅ Один корректный роутер с префиксом
router = APIRouter(prefix="/manager", tags=["manager"])

# 📋 Получить всех HVAC-сотрудников с фильтрацией
@router.get("/employees")
def get_employees(
    db: Session = Depends(get_db),
    status: str = Query(None),
    require_location: bool = Query(False),
):
    query = db.query(User).filter(User.role == 'hvac')

    if status:
        query = query.filter(User.status == status)
    if require_location:
        query = query.filter(User.location.isnot(None))

    employees = query.all()

    return [
        {
            "id": u.id,
            "name": u.name,
            "phone": u.phone,
            "qualification": u.qualification,
            "rate": u.rate,
            "tarif": u.tarif,
            "status": u.status,
            "location": u.location
        }
        for u in employees
    ]

# ✏️ Обновить HVAC-пользователя
@router.put("/users/{user_id}")
def update_hvac_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.role == 'hvac').first()
    if not user:
        raise HTTPException(status_code=404, detail="HVAC-пользователь не найден")

    updated = update_user(db, user_id, user_data)
    return {
        "id": updated.id,
        "name": updated.name,
        "phone": updated.phone,
        "qualification": updated.qualification,
        "status": updated.status
    }

# 📦 Получить список использования материалов
@router.get("/material-usage")
def get_material_usage(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Access denied")
    
    usage_records = db.query(MaterialUsage).all()

    result = []
    for usage in usage_records:
        result.append({
            "id": usage.id,
            "hvac_id": usage.hvac_id,
            "hvac_name": usage.hvac.name if usage.hvac else "—",
            "material_name": usage.name,
            "brand": usage.brand,
            "model": usage.model,
            "order_id": usage.order_id,
            "quantity_used": usage.quantity_used,
            "price_mxn": usage.price_mxn,
            "used_date": usage.used_date,
        })
    return result
