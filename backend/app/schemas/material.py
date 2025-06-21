from pydantic import BaseModel
from datetime import date

class MaterialSchema(BaseModel):
    id: int
    name: str
    brand: str | None = None
    model: str | None = None  # 🔧 Рекомендуется добавить (отсутствует в БД, но нужен на фронте)
    material_type: str | None = None
    specs: str | None = None
    price_usd: float | None = None
    price_mxn: float | None = None
    stock: int
    photo_url: str | None = None
    arrival_date: date | None = None
    issued_date: date | None = None
    issued_to_hvac: int | None = None
    qty_issued: int | None = None
    status: str | None = None

    class Config:
        from_attributes = True
