from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/manager/tariffs",
    tags=["manager-tariffs"]
)

# ======================================================
# Payloads
# ======================================================

class RoadTarifPayload(BaseModel):
    tarif: int   # цена дороги / вызова (за км)


class MaterialsRatePayload(BaseModel):
    rate: int    # % от стоимости материалов (оплата работы)


# ======================================================
# APPLY ROAD TARIF FOR ALL HVAC IN ORGANIZATION
# ======================================================
@router.put("/apply-road-tarif")
def apply_road_tarif_for_org(
    payload: RoadTarifPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can change tariffs")

    if not current_user.organization:
        raise HTTPException(status_code=400, detail="Manager has no organization")

    q = (
        db.query(User)
        .filter(User.role == "hvac")
        .filter(User.organization == current_user.organization)
    )

    updated = q.update(
        {User.tarif: payload.tarif},
        synchronize_session=False
    )

    db.commit()

    return {
        "status": "ok",
        "organization": current_user.organization,
        "updated_count": updated,
        "tarif": payload.tarif,
    }


# ======================================================
# APPLY MATERIALS RATE FOR ALL HVAC IN ORGANIZATION
# ======================================================
@router.put("/apply-materials-rate")
def apply_materials_rate_for_org(
    payload: MaterialsRatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can change tariffs")

    if not current_user.organization:
        raise HTTPException(status_code=400, detail="Manager has no organization")

    q = (
        db.query(User)
        .filter(User.role == "hvac")
        .filter(User.organization == current_user.organization)
    )

    updated = q.update(
        {User.qualification: payload.rate},
        synchronize_session=False
    )
 
    db.commit()

    return {
        "status": "ok",
        "organization": current_user.organization,
        "updated_count": updated,
        "rate": payload.rate,
    }
