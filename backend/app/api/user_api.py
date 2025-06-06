from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate
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
        qualification=user_data.qualification,
        rate=user_data.rate,
        status=user_data.status,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно зарегистрирован"}

# 🔍 Получение текущего пользователя (для /users/me)
@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "role": current_user.role,
        "location": current_user.location,
        "qualification": current_user.qualification,
        "rate": current_user.rate,
        "status": current_user.status,
    }
