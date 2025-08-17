from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
    role: str
    location: Optional[str] = None
    qualification: Optional[str] = None
    rate: Optional[int] = None
    status: Optional[str] = None
    tarif: Optional[int] = 20   # ← добавляем тут

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    qualification: Optional[str] = None
    rate: Optional[float] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    status: Optional[str] = None
    tarif: Optional[int] = None   # ← и тут
    
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
