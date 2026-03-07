from pydantic import BaseModel
from datetime import datetime

class FreeOrderCreate(BaseModel):
    address: str
    lat: float | None = None
    lng: float | None = None
    description: str | None = None
    payment_type: str | None = None
    currency: str | None = "USD"
    client_datetime: datetime | None = None
