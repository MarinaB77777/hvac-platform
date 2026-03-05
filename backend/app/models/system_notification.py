from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.db import Base


class SystemNotification(Base):
    __tablename__ = "system_notifications"

    id = Column(Integer, primary_key=True, index=True)

    # получатель (клиент)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # контекст (не меняем orders, просто ссылка)
    order_id = Column(Integer, nullable=True, index=True)

    # тип события
    type = Column(String, nullable=False)

    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
