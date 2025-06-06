from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str                     # отображаемое имя (для всех)
    phone: str                    # логин (используется при входе)
    password: str                 # обычный пароль (будет захеширован)
    role: str = "hvac"            # по умолчанию "hvac", но может быть "client", "manager" и т.д.

    # Дополнительные поля — используются только для HVAC и менеджера
    location: Optional[str] = None
    qualification: Optional[str] = None
    rate: Optional[int] = None
    status: Optional[str] = "active"   # можно оставить как "active" по умолчанию
