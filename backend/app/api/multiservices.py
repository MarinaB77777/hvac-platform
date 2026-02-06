# backend/app/api/multiservices.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.multiservice import MultiService
from app.schemas.multiservice import MultiServiceCreate, MultiServiceOut

router = APIRouter(prefix="/multiservices", tags=["multiservices"])


# =========================================================
# ✅ 1) GLOBAL LIST (for admin/debug)
#    Возвращает ВСЕ услуги из БД.
#    Использовать только для отладки/админов.
# =========================================================
@router.get("/all", response_model=list[MultiServiceOut])
def list_multiservices_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔒 Чтобы случайно не светить всем — ограничим правами
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    return db.query(MultiService).order_by(MultiService.id.asc()).all()


# =========================================================
# ✅ 2) ORG LIST (production)
#    Возвращает услуги ТОЛЬКО текущей организации.
# =========================================================
@router.get("/", response_model=list[MultiServiceOut])
def list_multiservices_org(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.organization:
        return []

    # 1) берём услуги организации
    q = (
        db.query(MultiService)
        .filter(MultiService.organization == current_user.organization)
        .order_by(MultiService.id.asc())
    )
    items = q.all()

    # 2) если пусто — создаём дефолтный HVAC (1 раз)
    if not items and current_user.role == "manager":
        try:
            last_id = db.query(func.max(MultiService.id)).scalar() or 0
            code = f"multiservice-{last_id + 1:06d}"

            ms = MultiService(
                organization=current_user.organization,
                multiservice_code=code,
                title="HVAC",
                details=None,
                road_tariff=None,          # НЕ трогаем вашу текущую логику
                diagnostic_price=None,     # сюда потом запишем DIAGNOSTIC_COST через UI
                materials_default=None,
                base_price=None,
                created_by_user_id=current_user.id,
                is_used=False,
            )
            db.add(ms)
            db.commit()
        except IntegrityError:
            db.rollback()

        # перечитываем список
        items = q.all()

    return items


@router.post("/", response_model=MultiServiceOut, status_code=201)
def create_multiservice(
    payload: MultiServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can create multiservices")

    if not current_user.organization:
        raise HTTPException(status_code=400, detail="Manager has no organization")

    last_id = db.query(func.max(MultiService.id)).scalar() or 0
    code = f"multiservice-{last_id + 1:06d}"

    ms = MultiService(
        organization=current_user.organization,  # ✅ ключевое
        multiservice_code=code,
        title=payload.title.strip(),
        details=(payload.details.strip() if payload.details else None),

        # тарифы/цены
        road_tariff=payload.road_tariff,
        diagnostic_price=payload.diagnostic_price,
        materials_default=payload.materials_default,
        base_price=payload.base_price,

        created_by_user_id=current_user.id,
        is_used=False,
    )

    db.add(ms)
    db.commit()
    db.refresh(ms)
    return ms


@router.delete("/{multiservice_id}")
def delete_multiservice(
    multiservice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can delete multiservices")

    ms = db.query(MultiService).filter(MultiService.id == multiservice_id).first()
    if not ms:
        raise HTTPException(status_code=404, detail="MultiService not found")

    # 🔒 организация должна совпадать
    if ms.organization != current_user.organization:
        raise HTTPException(status_code=403, detail="Not your organization")

    # 🔒 удалять может только создатель
    if ms.created_by_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can delete only your multiservices")

    if ms.is_used:
        raise HTTPException(status_code=409, detail="MultiService already used and cannot be deleted")

    db.delete(ms)
    db.commit()
    return {"status": "ok", "deleted_id": multiservice_id}
