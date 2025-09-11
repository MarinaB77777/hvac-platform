# models/organization.py
from sqlalchemy import Column, Integer, String
from app.db import Base

class Organization(Base):
    __tablename__ = "organization"

     id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    website = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    
    password_hash = Column(String, nullable=False)
    role = Column(String, default="organization")
