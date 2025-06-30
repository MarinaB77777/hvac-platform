from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import get_current_user

router = APIRouter()

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

@router.patch("/users/me")
def update_me(
    rate: Optional[int] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # HVAC может менять только свободен / не доступен вручную
    allowed_statuses = ["свободен", "не доступен"]
    if status and status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Нельзя вручную установить этот статус")

    if rate is not None:
        current_user.rate = rate
    if status:
        current_user.status = status
    if location:
        current_user.location = location
    if latitude is not None:
        current_user.latitude = latitude
    if longitude is not None:
        current_user.longitude = longitude

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при обновлении профиля")

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

@router.post("/users/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not bcrypt.verify(old_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Старый пароль неверен")

    current_user.hashed_password = bcrypt.hash(new_password)
    db.commit()
    return {"message": "Пароль успешно изменён"}
