# backend/app/api/personal_multiservices.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.multiservice import MultiService
from app.schemas.multiservice import MultiServiceCreate, MultiServiceOut
from app.services.personal_org import personal_org

router = APIRouter(prefix="/personal/multiservices", tags=["personal-multiservices"])


def resolve_hvac_id(current_user: User, hvac_id_query: int | None):
    role = current_user.role
    uid = current_user.id

    if role == "hvac":
        return uid

    if role == "warehouse":
        if not hvac_id_query:
            raise HTTPException(status_code=400, detail="hvac_id is required for warehouse")
        return hvac_id_query

    raise HTTPException(status_code=403, detail="Not allowed")


@router.get("/", response_model=list[MultiServiceOut])
def list_personal_multiservices(
    hvac_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hvac_id_final = resolve_hvac_id(current_user, hvac_id)
    org = personal_org(hvac_id_final)

    q = (
        db.query(MultiService)
        .filter(MultiService.organization == org)
        .order_by(MultiService.id.asc())
    )
    items = q.all()

    # автосоздание дефолтной строки HVAC (как у менеджера), но для personal-org
    if not items and current_user.role == "hvac":
        try:
            last_id = db.query(func.max(MultiService.id)).scalar() or 0
            code = f"multiservice-{last_id + 1:06d}"

            ms = MultiService(
                organization=org,
                multiservice_code=code,
                title="HVAC",
                details=None,
                road_tariff=None,
                diagnostic_price=200,  # дефолт на старте
                materials_default=None,
                base_price=None,
                created_by_user_id=current_user.id,
                is_used=False,
            )
            db.add(ms)
            db.commit()
        except IntegrityError:
            db.rollback()

        items = q.all()

    return items


@router.post("/", response_model=MultiServiceOut, status_code=201)
def upsert_personal_multiservice(
    payload: MultiServiceCreate,
    hvac_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hvac_id_final = resolve_hvac_id(current_user, hvac_id)
    org = personal_org(hvac_id_final)

    title = (payload.title or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    existing = (
        db.query(MultiService)
        .filter(MultiService.organization == org)
        .filter(func.lower(MultiService.title) == func.lower(title))
        .first()
    )

    if existing:
        if payload.details is not None:
            existing.details = payload.details.strip() if payload.details else None
        if payload.road_tariff is not None:
            existing.road_tariff = payload.road_tariff
        if payload.diagnostic_price is not None:
            existing.diagnostic_price = payload.diagnostic_price
        if payload.materials_default is not None:
            existing.materials_default = payload.materials_default
        if payload.base_price is not None:
            existing.base_price = payload.base_price

        existing.created_by_user_id = existing.created_by_user_id or current_user.id
        db.commit()
        db.refresh(existing)
        return existing

    last_id = db.query(func.max(MultiService.id)).scalar() or 0
    code = f"multiservice-{last_id + 1:06d}"

    ms = MultiService(
        organization=org,
        multiservice_code=code,
        title=title,
        details=(payload.details.strip() if payload.details else None),
        road_tariff=payload.road_tariff,
        diagnostic_price=payload.diagnostic_price,
        materials_default=payload.materials_default,
        base_price=payload.base_price,
        created_by_user_id=current_user.id,
        is_used=False,
    )

    db.add(ms)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="MultiService already exists")

    db.refresh(ms)
    return ms
