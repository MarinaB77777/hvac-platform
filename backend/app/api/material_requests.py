# app/api/material_requests.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.material import Material
from app.models.material_request import MaterialRequest
from app.schemas.material_request import MaterialRequestCreate, MaterialRequestOut

router = APIRouter(prefix="/material-requests", tags=["Material Requests"])


# 🔹 Создать заявку на материал (HVAC)
@router.post("/", response_model=MaterialRequestOut)
def create_material_request(
    request_in: MaterialRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create requests")

    material = db.query(Material).filter(Material.id == request_in.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    request = MaterialRequest(
        material_id=request_in.material_id,
        order_id=request_in.order_id,
        hvac_id=current_user.id,
        quantity=request_in.quantity,
        status="pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


# 🔹 Получить все заявки (warehouse)
@router.get("/", response_model=List[MaterialRequestOut])
def list_all_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can view all requests")
    return db.query(MaterialRequest).all()


# 🔹 Подтвердить заявку (warehouse)
@router.post("/{request_id}/confirm", response_model=MaterialRequestOut)
def confirm_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can confirm requests")

    request = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = "confirmed"
    db.commit()
    db.refresh(request)
    return request


# 🔹 Выдать материал по заявке и обновить qty_issued
@router.post("/{request_id}/issue", response_model=MaterialRequestOut)
def issue_material(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can issue materials")

    request = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status != "confirmed":
        raise HTTPException(status_code=400, detail="Request must be confirmed first")

    material = db.query(Material).filter(Material.id == request.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Обновить qty_issued
    material.qty_issued += request.quantity
    request.status = "issued"

    db.commit()
    db.refresh(request)
    return request


# 🔹 Получить свои заявки (HVAC)
@router.get("/my-requests", response_model=List[MaterialRequestOut])
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can view their own requests")

    return db.query(MaterialRequest).filter(MaterialRequest.hvac_id == current_user.id).all()


# 🔹 Получить заявки по конкретному заказу
@router.get("/by-order/{order_id}", response_model=List[MaterialRequestOut])
def get_requests_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_roles = ["warehouse", "manager", "hvac"]
    if current_user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied")

    query = db.query(MaterialRequest).filter(MaterialRequest.order_id == order_id)

    if current_user.role == "hvac":
        query = query.filter(MaterialRequest.hvac_id == current_user.id)

    return query.all()
