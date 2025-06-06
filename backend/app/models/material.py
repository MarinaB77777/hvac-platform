from sqlalchemy import Column, Integer, String
from app.db import Base

class Material(Base):
    tablename = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    stock_count = Column(Integer)
    photo_url = Column(String)
    status = Column(String)
    arrival_date = Column(String)  # Можно заменить на Date, если используешь формат даты
