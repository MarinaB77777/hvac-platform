from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ManagerTaskCreate(BaseModel):
    hvac_id: int
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    materials_note: Optional[str] = None


class ManagerTaskOut(BaseModel):
    id: int
    organization: Optional[str] = None

    manager_id: int
    hvac_id: int

    title: str
    description: Optional[str] = None

    due_datetime: Optional[datetime] = None
    materials_note: Optional[str] = None

    hvac_comment: Optional[str] = None
    manager_comment: Optional[str] = None

    result_files: Optional[str] = None

    status: str

    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
