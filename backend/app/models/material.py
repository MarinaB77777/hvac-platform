# app/models/material.py
from sqlalchemy import Column, Integer, String, Date, Text
from app.db import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    material_type = Column(String, nullable=True)  # заменили category
    specs = Column(String, nullable=True)
    price_usd = Column(Integer, nullable=True)
    price_mxn = Column(Integer, nullable=True)
    stock = Column(Integer, nullable=True)
    photo_url = Column(String, nullable=True)
    arrival_date = Column(Date, nullable=True)
    status = Column(String, nullable=True)
