from sqlalchemy import Column, Integer, String, Date
from app.db import Base
from datetime import datetime

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    stock_count = Column(Integer)
    photo_url = Column(String)
    status = Column(String)
    arrival_date = Column(Date, default=datetime.utcnow)  # ✅ автоматическая дата
