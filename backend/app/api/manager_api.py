from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserUpdate

router = APIRouter()


# 🔍 Получить всех сотрудников с ролью 'hvac'
@router.get("/manager/employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(User).filter(User.role == 'hvac').all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "phone": u.phone,
            "qualification": u.qualification,
            "rate": u.rate,
            "status": u.status,
            "password": u.hashed_password,  # хэш пароля
        }
        for u in employees
    ]


# 📝 Обновить информацию сотрудника
@router.put("/manager/employees/{user_id}")
def update_employee(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db)):
    employee = db.query(User).filter(User.id == user_id, User.role == 'hvac').first()

    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    employee.name = updated_data.name
    employee.phone = updated_data.phone
    employee.qualification = updated_data.qualification
    employee.rate = updated_data.rate
    employee.status = updated_data.status

    if updated_data.password:
        employee.hashed_password = bcrypt.hash(updated_data.password)

    db.commit()
    db.refresh(employee)

    return {"message": "Сотрудник обновлён"}
