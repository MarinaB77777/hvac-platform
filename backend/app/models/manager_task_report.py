from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db import Base


class ManagerTaskReport(Base):
    __tablename__ = "manager_task_reports"

    id = Column(Integer, primary_key=True, index=True)

    # связь с задачей
    task_id = Column(Integer, ForeignKey("manager_tasks.id"), nullable=False, index=True)

    # кто отправил
    hvac_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # данные отчета
    result_files = Column(String, nullable=True)     # JSON строка (как сейчас)
    hvac_comment = Column(String, nullable=True)
    materials_note = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
