from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.services.user_service import update_user
from app.schemas.user import UserUpdate

router = APIRouter()

# 📋 Получить всех HVAC-сотрудников с фильтрацией
@router.get("/manager/employees")
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
