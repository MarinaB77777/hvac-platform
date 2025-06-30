from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import get_current_user

router = APIRouter()

# 🔐 Регистрация
@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = bcrypt.hash(user_data.password)

    new_user = User(
        name=user_data.name,
        phone=user_data.phone,
        hashed_password=hashed_password,
        role=user_data.role,
        location=user_data.location,
        qualification=user_data.qualification or None,
        rate=user_data.rate if user_data.rate is not None else None,
        status=user_data.status or "active",
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении пользователя: {str(e)}")

    return {"message": "Пользователь успешно зарегистрирован", "id": new_user.id}


# 🔍 Получение текущего пользователя
@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "role": current_user.role,
        "location": current_user.location,
        "latitude": current_user.latitude,
        "longitude": current_user.longitude,
        "qualification": current_user.qualification,
        "rate": current_user.rate,
        "status": current_user.status,
    }


# ✏️ Обновление данных текущего пользователя
@router.patch("/users/me")
def update_me(update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    update_fields = update_data.dict(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(current_user, field, value)

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления данных: {str(e)}")

    return {
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "role": current_user.role,
        "location": current_user.location,
        "latitude": current_user.latitude,
        "longitude": current_user.longitude,
        "qualification": current_user.qualification,
        "rate": current_user.rate,
        "status": current_user.status,
    }
