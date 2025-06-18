from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.db import get_db
from app.models.user import User

# 🔐 Константы
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 💡 Используем tokenUrl для формы логина
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 📦 Создание JWT-токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔍 Получение пользователя по телефону
def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()


# ✅ Проверка пароля
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)


# 🔑 Аутентификация по телефону и паролю
def authenticate_user(db: Session, phone: str, password: str):
    user = get_user_by_phone(db, phone)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# 👤 Получение текущего пользователя из токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("🔍 Получен токен:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        print("✅ Распознан user_id:", user_id)
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print("✅ Пользователь найден:", user.name)
        else:
            print("❌ Пользователь не найден")
        return user
    except JWTError as e:
        print("❌ JWT ошибка:", e)
        raise HTTPException(status_code=401, detail="Token invalid")
