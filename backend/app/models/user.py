from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Boolean, DateTime, Float
from app.db import Base

class UserRole(str, Enum):
    client = "client"
    hvac = "hvac"
    warehouse = "warehouse"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)                         # отображаемое имя
    phone = Column(String, unique=True, index=True, nullable=False)  # логин
    hashed_password = Column(String, nullable=False)              # хэш пароля
    role = Column(SQLEnum(UserRole), nullable=False)              # тип пользователя
    
    # Новые поля
    location = Column(String, nullable=True)                      # местоположение
    qualification = Column(String, nullable=True)                 # квалификация (HVAC)
    rate = Column(Integer, nullable=True)                         # тариф или ставка
    status = Column(String, nullable=True)                        # активен / заблокирован / уволен и т.п.
    address = Column(String, nullable=True)
    tarif = Column(Float, default=20.0)  # процент от стоимости расходников
