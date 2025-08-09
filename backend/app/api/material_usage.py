# app/api/material_usage.py 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db import get_db
from app.services.auth import get_current_user
from app.models.material_usage import MaterialUsage
from app.models.material import Material                    # ← ДОБАВИТЬ
from app.schemas.material_usage import MaterialUsageCreate, MaterialUsageOut
from app.models.user import User

router = APIRouter(prefix="/material-usage", tags=["Material Usage"])

@router.post("/", response_model=MaterialUsageOut)
def create_usage(
    usage_in: MaterialUsageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create usage entries")

    material = db.query(Material).filter(Material.id == usage_in.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    usage = MaterialUsage(
        hvac_id=usage_in.hvac_id,
        order_id=usage_in.order_id,
        material_id=usage_in.material_id,
        quantity_used=usage_in.quantity_used,
        used_date=datetime.utcnow(),           # ← фиксируем дату списания
        # копии свойств на момент списания
        name=material.name,
        brand=material.brand,
        model=material.model,
        specs=material.specs,
        price_usd=material.price_usd,
        price_mxn=material.price_mxn,
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)
    return usage
