from enum import Enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from app.db import Base

Base = declarative_base()

class UserRole(str, Enum):
    client = "client"
    hvac = "hvac"
    warehouse = "warehouse"
    manager = "manager"

class User(Base):
    __tablename__ = "users"  # <-- исправлено здесь

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
