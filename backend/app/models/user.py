from sqlalchemy import Column, String, Integer
from app.db import Base

class User(Base):
    __tablename__ = "users"  # ✅ правильно пишем имя таблицы с двумя подчёркиваниями

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)                   # отображаемое имя
    phone = Column(String, unique=True, index=True)         # логин (телефон)
    hashed_password = Column(String, nullable=False)        # хэш пароля
    role = Column(String, nullable=False)                   # роль (hvac и т.д.)
