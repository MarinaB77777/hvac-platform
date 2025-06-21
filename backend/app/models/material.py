# app/models/material.py

from sqlalchemy import Column, Integer, String, Float, Date
from app.db import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)

    # Основные поля
    name = Column(String, nullable=False)                  # Название расходника: "Компрессор", "Фреон", "Трансформатор"
    brand = Column(String, nullable=True)                  # Бренд (например, Embraco), может быть пустым
    # model = Column(String, nullable=True)                  # Модель или марка (например, R404a, NJ9238GK)
    material_type = Column(String, nullable=True)          # Тип: "компрессор", "фреон", и т.д.
    specs = Column(String, nullable=True, comment="Описание: напряжение, температурный режим, применение и др.")

    # Цены
    price_usd = Column(Float, nullable=True)               # Цена в долларах
    price_mxn = Column(Float, nullable=True)               # Цена в мексиканских песо

    # Склад
    stock = Column(Integer, nullable=False, default=0)     # Кол-во на складе
    photo_url = Column(String, nullable=True)              # Фото (URL)

    # Хронология и выдача
    arrival_date = Column(Date, nullable=True)             # Дата поступления на склад
    issued_date = Column(Date, nullable=True)              # Дата выдачи HVAC-сотруднику
    issued_to_hvac = Column(Integer, nullable=True)        # ID HVAC-сотрудника, получившего материал
    qty_issued = Column(Integer, nullable=True)            # Кол-во выданное этому сотруднику

    # Статус
    status = Column(String, default="available")           # Текущий статус: available, used, reserved и др.
