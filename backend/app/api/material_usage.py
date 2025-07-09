from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.services.auth import get_current_user
from app.models.material_usage import MaterialUsage
from app.schemas.material_usage import MaterialUsageCreate, MaterialUsageOut
from app.models.user import User

router = APIRouter(prefix="/material-usage", tags=["Material Usage"])

# 🔹 Создание записи использования материала
@router.post("/", response_model=MaterialUsageOut)
def create_usage(
    usage_in: MaterialUsageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create usage entries")

    usage = MaterialUsage(**usage_in.dict())
    db.add(usage)
    db.commit()
    db.refresh(usage)
    return usage

# 🔹 Получить все использования текущего HVAC
@router.get("/by-hvac/{hvac_id}", response_model=List[MaterialUsageOut])
def get_by_hvac(
    hvac_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["hvac", "manager", "warehouse"]:
        raise HTTPException(status_code=403, detail="Access denied")

    return db.query(MaterialUsage).filter(MaterialUsage.hvac_id == hvac_id).all()
