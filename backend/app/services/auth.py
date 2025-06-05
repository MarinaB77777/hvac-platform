from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.db import get_db
from app.models.user import User

# Константы
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Схема авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔐 Создание токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔍 Получение пользователя по имени
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()

# ✅ Проверка пароля
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

# 🚪 Аутентификация пользователя
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# 👤 Получение текущего пользователя по токену
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user_by_username(db, username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
