from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material

router = APIRouter()

# 📦 Получить материалы со склада с фильтрацией
@router.get("/materials")
def get_all_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "model": m.model,
            "brand": m.brand,
            "material_type": m.material_type,
            "specs": m.specs,
            "price_usd": m.price_usd,
            "price_mxn": m.price_mxn,
            "stock": m.stock,
            "photo_url": m.photo_url,
            "arrival_date": m.arrival_date,
            "issued_date": m.issued_date,
            "issued_to_hvac": m.issued_to_hvac,
            "qty_issued": m.qty_issued,
            "status": m.status,
        }
        for m in materials
    ]
