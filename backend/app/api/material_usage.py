from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db import get_db
from app.services.auth import get_current_user
from app.models.material_usage import MaterialUsage
from app.schemas.material_usage import MaterialUsageCreate, MaterialUsageOut
from app.models.user import User

router = APIRouter(prefix="/material-usage", tags=["Material Usage"])


def serialize_usage(usage: MaterialUsage) -> dict:
    """
    Возвращаем словарь, который соответствует Pydantic-схеме MaterialUsageOut,
    и при этом аккуратно маппим used_date -> used_at.
    Дополнительно кладём "qty_used" и "cost" для фронта (лишние поля модель отбросит).
    """
    return {
        "id": usage.id,
        "hvac_id": usage.hvac_id,
        "order_id": usage.order_id,
        "material_id": usage.material_id,
        "quantity_used": usage.quantity_used,
        # дублируем для фронта, который иногда читает qty_used
        "qty_used": usage.quantity_used,
        # Pydantic ждёт used_at — даём его из used_date
        "used_at": usage.used_date,
        # копии атрибутов материала (если есть)
        "name": usage.name,
        "brand": usage.brand,
        "model": usage.model,
        "specs": usage.specs,
        "price_usd": usage.price_usd,
        "price_mxn": usage.price_mxn,
        # Иногда фронт ожидает "cost" — подставим MXN если есть, иначе USD
        "cost": usage.price_mxn if usage.price_mxn is not None else usage.price_usd,
    }


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

    # На всякий случай проставим время, если БД по какой-то причине не выставит default
    if usage.used_date is None:
        usage.used_date = datetime.utcnow()

    db.add(usage)
    db.commit()
    db.refresh(usage)
    return serialize_usage(usage)


# 🔹 Получить использования текущего HVAC (опц. фильтр по заказу)
@router.get("/by-hvac/{hvac_id}", response_model=List[MaterialUsageOut])
def get_by_hvac(
    hvac_id: int,
    order_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["hvac", "manager", "warehouse"]:
        raise HTTPException(status_code=403, detail="Access denied")

    query = db.query(MaterialUsage).filter(MaterialUsage.hvac_id == hvac_id)
    if order_id is not None:
        query = query.filter(MaterialUsage.order_id == order_id)

    usages = query.all()
    return [serialize_usage(u) for u in usages]
