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

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    qualification: Optional[str] = None
    rate: Optional[int] = None
    status: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserOut(BaseModel):
    id: int
    name: str
    phone: str
    role: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    qualification: Optional[str] = None
    rate: Optional[int] = None
    status: Optional[str] = None

 model_config = {
        "from_attributes": True
    }



