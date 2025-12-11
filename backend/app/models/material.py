# backend/app/models/material.py
from sqlalchemy import Column, Integer, String, Float, Date
from app.db import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    specs = Column(String, nullable=True)
    price_usd = Column(Float, nullable=True)
    price_mxn = Column(Float, nullable=True)
    stock = Column(Integer, nullable=True)
    photo_url = Column(String, nullable=True)
    arrival_date = Column(Date, nullable=True)
    issued_date = Column(Date, nullable=True)
    issued_to_hvac = Column(Integer, nullable=True)
    qty_issued = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
