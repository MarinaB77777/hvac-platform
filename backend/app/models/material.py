# app/models/material.py

from sqlalchemy import Column, Integer, String, Date
from app.db import Base
from datetime import datetime

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)  # уникальный идентификатор
    name = Column(String, nullable=False)               # наименование материала
    brand = Column(String)                              # бренд
    category = Column(String)                           # категория (фреон, компрессор и т.д.)
    specs = Column(String)                              # характеристики или модель
    price_usd = Column(Integer)                         # цена в долларах
    price_mxn = Column(Integer)                         # цена в мексиканских песо
    stock = Column(Integer, default=0)                  # количество на складе
    photo_url = Column(String)                          # ссылка на изображение
    arrival_date = Column(Date, default=datetime.utcnow) # дата поступления
    status = Column(String, default="available")        # статус материала (например: available, issued)
