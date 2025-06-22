from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material

router = APIRouter()

# 📦 Получить материалы со склада с фильтрацией
@router.get("/warehouse/materials")
def get_warehouse_materials(
    db: Session = Depends(get_db),
    material_type: str = Query(None),
    brand: str = Query(None),
    in_stock_only: bool = Query(False),
):
    query = db.query(Material)

    if material_type:
        query = query.filter(Material.material_type.ilike(f"%{material_type}%"))
    if brand:
        query = query.filter(Material.brand.ilike(f"%{brand}%"))
    if in_stock_only:
        query = query.filter(Material.stock > 0)

    materials = query.all()

    return [
        {
            "id": m.id,
            "name": m.name,
            "material_type": m.material_type,
            "brand": m.brand,
            "specs": m.specs,
            "price_usd": m.price_usd,
            "price_mxn": m.price_mxn,
            "stock": m.stock,
            "photo_url": m.photo_url,
            "arrival_date": m.arrival_date.isoformat() if m.arrival_date else None,
            "issued_date": m.issued_date.isoformat() if m.issued_date else None,
            "issued_to_hvac": m.issued_to_hvac,
            "qty_issued": m.qty_issued,
            "status": m.status,
        }
        for m in materials
    ]
