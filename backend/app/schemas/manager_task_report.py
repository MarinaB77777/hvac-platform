from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ManagerTaskReportCreate(BaseModel):
    task_id: int
    result_files: Optional[str] = None
    hvac_comment: Optional[str] = None
    materials_note: Optional[str] = None


class ManagerTaskReportOut(BaseModel):
    id: int
    task_id: int
    hvac_id: int

    result_files: Optional[str] = None
    hvac_comment: Optional[str] = None
    materials_note: Optional[str] = None

    created_at: datetime

    class Config:
        from_attributes = True
