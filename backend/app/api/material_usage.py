from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.services.auth import get_current_user
from app.models.material_usage import MaterialUsage
from app.models.material import Material
from app.models.user import User
from app.schemas.material_usage import MaterialUsageCreate, MaterialUsageOut

router = APIRouter(prefix="/material-usage", tags=["Material Usage"])


# ─────────────────────────────────────────────────────────────
# Создание записи использования материала
# ─────────────────────────────────────────────────────────────
@router.post("/", response_model=MaterialUsageOut)
def create_usage(
    usage_in: MaterialUsageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # только HVAC может списывать
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create usage entries")

    # элементарная валидация
    if usage_in.quantity_used <= 0:
        raise HTTPException(status_code=422, detail="quantity_used must be > 0")

    # подтянуть материал и снять "снимок" цен/атрибутов
    material = db.query(Material).filter(Material.id == usage_in.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    usage = MaterialUsage(
        hvac_id=usage_in.hvac_id,
        order_id=usage_in.order_id,
        material_id=usage_in.material_id,
        quantity_used=usage_in.quantity_used,
        # snapshot полей на момент списания:
        name=material.name,
        brand=material.brand,
        model=material.model,
        specs=material.specs,
        price_usd=material.price_usd,
        price_mxn=material.price_mxn,
        # used_date не трогаем — default=datetime.utcnow в модели
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)

    # Если в схеме поле называется иначе (например, used_at),
    # FastAPI сам сматчит, если в Pydantic настроен from_attributes.
    # Возвращаем ORM-объект — это совместимо с текущей схемой проекта.
    return usage


# ─────────────────────────────────────────────────────────────
# Получить использования по HVAC (с опциональным фильтром по заказу)
# ─────────────────────────────────────────────────────────────
@router.get("/by-hvac/{hvac_id}", response_model=List[MaterialUsageOut])
def get_by_hvac(
    hvac_id: int,
    order_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # доступ: hvac / manager / warehouse
    if current_user.role not in ("hvac", "manager", "warehouse"):
        raise HTTPException(status_code=403, detail="Access denied")

    q = db.query(MaterialUsage).filter(MaterialUsage.hvac_id == hvac_id)
    if order_id is not None:
        q = q.filter(MaterialUsage.order_id == order_id)

    # для удобства — свежие сверху
    q = q.order_by(MaterialUsage.used_date.desc())

    return q.all()
