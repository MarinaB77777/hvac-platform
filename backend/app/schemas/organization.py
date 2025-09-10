from pydantic import BaseModel
from typing import Optional

class OrganizationCreate(BaseModel):
    name: str
    phone: str
    password: str  # 🔐 теперь организация указывает пароль при регистрации
    description: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None

class OrganizationOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    website: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    model_config = {
        "from_attributes": True
    }

class OrganizationUpdate(BaseModel):
    name: str
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class OrganizationLogin(BaseModel):
    phone: str
    password: str

    model_config = {
        "from_attributes": True
    }
