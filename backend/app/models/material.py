from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/materials/")
def get_all_materials(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] not in ["warehouse", "hvac", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    materials = db.query(Material).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "brand": m.brand,
            "stock": m.stock,
            "category": m.category,
            "specs": m.specs,
            "price_usd": m.price_usd,
            "price_mxn": m.price_mxn,
            "photo_url": m.photo_url,
            "arrival_date": m.arrival_date.isoformat() if m.arrival_date else None,
            "status": m.status,
        }
        for m in materials
    ]
