# models/organization.py
from sqlalchemy import Column, Integer, String
from app.db import Base

class Organization(Base):
    __tablename__ = "organization"  # 👈 ОБЯЗАТЕЛЬНО с двумя подчёркиваниями

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # Название
    phone = Column(String, unique=True, index=True, nullable=False) # Для входа
    password = Column(String, nullable=False)                       # Как у всех
    description = Column(String, nullable=True)
    website = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
