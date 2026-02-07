from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MultiServiceCreate(BaseModel):
    title: str
    details: Optional[str] = None

    road_tariff: Optional[int] = None
    diagnostic_price: Optional[int] = None
    materials_default: Optional[int] = None
    base_price: Optional[int] = None

class MultiServiceOut(BaseModel):
    id: int
    organization: Optional[str] = None
    multiservice_code: str
    title: str
    details: Optional[str] = None

    road_tariff: Optional[int] = None
    diagnostic_price: Optional[int] = None
    materials_default: Optional[int] = None
    base_price: Optional[int] = None

    created_by_user_id: Optional[int] = None
    is_used: bool

    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
