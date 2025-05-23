from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from datetime import datetime

Base = declarative_base()

class OrderStatus(str, Enum):
    new = "new"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    declined = "declined"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    hvac_id = Column(Integer, nullable=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.new)
    address = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
