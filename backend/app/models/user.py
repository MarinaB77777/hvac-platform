from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from app.db import Base

class UserRole(str, Enum):
    client = "client"
    hvac = "hvac"
    warehouse = "warehouse"
    manager = "manager"

class User(Base):
    tablename = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    hashed_password = Column(String, nullable=False)  # ← ДОБАВИТЬ
