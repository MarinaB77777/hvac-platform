from sqlalchemy import Column, Integer, String, Date
from app.db import Base
from datetime import datetime

class Material(Base):
    __tablename__ = "materials"

materials_db = [
    {"id": 1, "name": "Фреон", "brand": "R410", "unit_price": 15},
    {"id": 2, "name": "Компрессор", "brand": "Hitachi", "unit_price": 120},
    {"id": 3, "name": "Фильтр", "brand": "Panasonic", "unit_price": 40},
    {"id": 4, "name": "Термостат", "brand": "Danfoss", "unit_price": 60}
]

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    stock_count = Column(Integer)
    photo_url = Column(String)
    status = Column(String)
    arrival_date = Column(Date, default=datetime.utcnow)  # ✅ автоматическая дата
