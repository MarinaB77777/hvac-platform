# backend/app/api/public_hvac_tariffs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.multiservice import MultiService
from app.services.personal_org import personal_org

router = APIRouter(prefix="/public/hvac-tariffs", tags=["public-hvac-tariffs"])

DEFAULT_DIAGNOSTIC = 200

@router.get("/{hvac_id}")
def get_tariffs_by_hvac_id(
    hvac_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),  # просто чтобы был токен
):
    hvac = db.query(User).filter(User.id == hvac_id).first()
    if not hvac:
        raise HTTPException(status_code=404, detail="HVAC not found")

    # 1) если у HVAC есть organization -> ищем в орг-таблице
    if hvac.organization:
        org = hvac.organization
    else:
        # 2) иначе -> personal:<hvac_id>
        org = personal_org(hvac_id)

    ms = (
        db.query(MultiService)
        .filter(MultiService.organization == org)
        .filter(func.lower(MultiService.title) == "hvac")
        .first()
    )

    diagnostic = ms.diagnostic_price if (ms and ms.diagnostic_price is not None) else DEFAULT_DIAGNOSTIC

    return {
        "hvac_id": hvac_id,
        "organization": org,
        "diagnostic_price": diagnostic,
        "road_tariff": ms.road_tariff if ms else None,
        "source": "multiservices" if (ms and ms.diagnostic_price is not None) else "fallback_200",
    }
