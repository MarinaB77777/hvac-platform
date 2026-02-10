from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.auth import get_current_user
from app.models.material import Material
from app.models.user import User
from app.services.personal_org import personal_org

router = APIRouter(prefix="/personal/materials", tags=["personal-warehouse"])


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


@router.get("/")
def list_personal_materials(
    hvac_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    hvac_id_final = resolve_hvac_id(current_user, hvac_id)
    org = personal_org(hvac_id_final)

    return (
        db.query(Material)
        .filter(Material.organization == org)
        .order_by(Material.id.desc())
        .all()
    )


@router.post("/")
def create_personal_material(
    payload: dict,
    hvac_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    hvac_id_final = resolve_hvac_id(current_user, hvac_id)
    org = personal_org(hvac_id_final)

    name = (payload.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    m = Material(
        name=name,
        brand=payload.get("brand"),
        model=payload.get("model"),
        specs=payload.get("specs"),
        price_usd=payload.get("price_usd"),
        price_mxn=payload.get("price_mxn"),
        stock=payload.get("stock"),
        photo_url=payload.get("photo_url"),
        arrival_date=payload.get("arrival_date"),
        status=payload.get("status"),
        organization=org,
        issued_to_hvac=hvac_id_final,
    )

    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.patch("/{material_id}")
def update_personal_material(
    material_id: int,
    payload: dict,
    hvac_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    hvac_id_final = resolve_hvac_id(current_user, hvac_id)
    org = personal_org(hvac_id_final)

    m = (
        db.query(Material)
        .filter(Material.id == material_id)
        .filter(Material.organization == org)
        .first()
    )
    if not m:
        raise HTTPException(status_code=404, detail="Material not found")

    # обновляем только то, что пришло
    for field in [
        "name", "brand", "model", "specs",
        "price_usd", "price_mxn", "stock",
        "photo_url", "arrival_date", "status"
    ]:
        if field in payload:
            val = payload.get(field)
            if field == "name" and val is not None:
                val = val.strip()
            setattr(m, field, val)

    db.commit()
    db.refresh(m)
    return m


@router.delete("/{material_id}")
def delete_personal_material(
    material_id: int,
    hvac_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    hvac_id_final = resolve_hvac_id(current_user, hvac_id)
    org = personal_org(hvac_id_final)

    m = (
        db.query(Material)
        .filter(Material.id == material_id)
        .filter(Material.organization == org)
        .first()
    )
    if not m:
        raise HTTPException(status_code=404, detail="Material not found")

    db.delete(m)
    db.commit()
    return {"status": "ok", "deleted_id": material_id}
