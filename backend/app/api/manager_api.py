from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User

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
            "status": u.status,
            "location": u.location
        }
        for u in employees
    ]
