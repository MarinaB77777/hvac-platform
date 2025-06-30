from enum import Enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum
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

class UserStatus(str, Enum):
    available = "свободен"
    working = "заказ выполняется"
    diagnosed = "диагностика завершена"
    accepted = "заказ принят"
    unavailable = "не доступен"
    
    # Новые поля
    location = Column(String, nullable=True)                      # местоположение
    latitude = Column(String, nullable=True)                      # широта
    longitude = Column(String, nullable=True)                     # долгота
    qualification = Column(String, nullable=True)                 # квалификация (HVAC)
    rate = Column(Integer, nullable=True)                         # тариф или ставка
    status = Column(String, nullable=True)                        # активен / заблокирован / уволен и т.п.
