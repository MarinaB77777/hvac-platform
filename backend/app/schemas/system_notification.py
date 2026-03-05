from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SystemNotificationCreate(BaseModel):
    order_id: int


class SystemNotificationOut(BaseModel):
    id: int
    order_id: Optional[int]
    type: str
    title: str
    body: str
    created_at: datetime
    read_at: Optional[datetime]

    class Config:
        orm_mode = True
