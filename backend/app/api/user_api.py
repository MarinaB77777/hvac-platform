from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
 

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, ChangePasswordRequest
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 🔍 Проверка — есть ли уже пользователь с таким телефоном
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    # 🔐 Хешируем пароль
    hashed_password = bcrypt.hash(user_data.password)

    # ✅ Создаём нового пользователя
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
        "address": current_user.address
    }
@router.patch("/users/me")
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 🔄 Координаты → сохраняем в location как строку "lat,lon"
    if user_update.location is not None:
    current_user.location = user_update.location

    # 🔄 Имя
    if user_update.name is not None:
        current_user.name = user_update.name

    # 🔄 Телефон
    if user_update.phone is not None:
        current_user.phone = user_update.phone

    # 🔄 Квалификация
    if user_update.qualification is not None:
        current_user.qualification = user_update.qualification

    # 🔄 Тариф
    if user_update.rate is not None:
        current_user.rate = user_update.rate

    # 🔄 Статус
    if user_update.status is not None:
        current_user.status = user_update.status

    # 🔄 Адрес
    if user_update.address is not None:
        current_user.address = user_update.address

    # 🔄 Роль (если вдруг нужно разрешить менять — по умолчанию не трогаем)
    if user_update.role is not None:
        current_user.role = user_update.role

    # ✅ Сохраняем
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Профиль обновлён",
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "role": current_user.role,
        "location": current_user.location,
        "qualification": current_user.qualification,
        "rate": current_user.rate,
        "status": current_user.status,
        "address": current_user.address
    }

@router.post("/users/change-password")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not bcrypt.verify(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")

    current_user.hashed_password = bcrypt.hash(data.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"message": "Пароль успешно обновлён"}
