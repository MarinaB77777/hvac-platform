from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
    role: str = "hvac"  # можно оставить фиксированной
