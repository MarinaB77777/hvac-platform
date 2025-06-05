from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = bcrypt.hash(user_data.password)

    new_user = User(
        name=user_data.username,
        hashed_password=hashed_password,
        role=user_data.role,
        phone=user_data.username  # если username — это телефон
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Пользователь успешно зарегистрирован", "id": new_user.id}
