from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db import get_db
from app.models.user import User
from app.services.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # ✅ Сравниваем по телефону, а не по имени
    user = db.query(User).filter(User.phone == form_data.username).first()

    if not user or not bcrypt.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    roles = [user.role]
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "role": user.role,          # базовая роль
            "organization": user.organization,
        }
    }


    
