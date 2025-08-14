from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from enum import Enum
from datetime import datetime
from app.db import Base  # Используем общий Base

# Возможные статусы заказа
class OrderStatus(str, Enum):
    new = "new"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    declined = "declined"

# Таблица заказов
class Order(Base):
    __tablename__ = "orders"  # ✅ Обязательно двойное подчёркивание

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)               # ID клиента (user_id)
    hvac_id = Column(Integer, nullable=True)                  # ID исполнителя (user_id)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.new)

    address = Column(String, nullable=False)                  # Адрес
    lat = Column(Float, nullable=True)                        # Геокоординаты
    lng = Column(Float, nullable=True)
    description = Column(String, nullable=True)               # Описание поломки

    diagnostic_url = Column(String, nullable=True)            # 📎 Файл диагностики
    result_file_url = Column(String, nullable=True)           # 📎 Файл результата работы
    client_agreed = Column(String, default="false")           # Согласие клиента
    
    # 💰 Компоненты стоимости
    diagnostic_cost = Column(Integer, nullable=True)        # Фиксированная стоимость диагностики
    distance_cost = Column(Integer, nullable=True)          # Стоимость дороги (расстояние * RATE_PER_KM)
    parts_cost = Column(Integer, nullable=True)             # Стоимость материалов (запчастей)

    # 💸 Общие итоговые суммы
    repair_cost = Column(Integer, nullable=True)            # 💡 Стоимость работы = parts_cost + 20%
    agreed_total_mxn = Column(Integer, nullable=True)       # 💵 Сумма, с которой клиент согласился (в MXN)
    
    # 💱 Валюта и способ оплаты
    currency = Column(String, nullable=True)                # Валюта заказа (например, 'USD' или 'MXN')
    payment_type = Column(String, nullable=True)            # Способ оплаты (например, 'наличные')

    created_at = Column(DateTime, default=datetime.utcnow)    # Дата создания
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)


