from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db import Base


class ManagerTask(Base):
    __tablename__ = "manager_tasks"

    id = Column(Integer, primary_key=True, index=True)

    # организация
    organization = Column(String, index=True, nullable=False)

    # кто назначил и кому назначено
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hvac_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # задача
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # срок выполнения
    due_datetime = Column(DateTime(timezone=True), nullable=True)

    # что нужно для выполнения
    materials_note = Column(String, nullable=True)

    # комментарии
    hvac_comment = Column(String, nullable=True)
    manager_comment = Column(String, nullable=True)

    # фотоотчёт (JSON string, как в orders)
    result_files = Column(String, nullable=True)

    # new / done / needs_rework
    status = Column(String, default="new", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
