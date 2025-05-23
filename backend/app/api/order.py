from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.order import (
    create_order,
    get_order_by_id,
    list_available_orders,
    accept_order,
    complete_order,
    get_orders_for_hvac,
    upload_result_file,
    upload_diagnostic_file,
    rate_order,
    update_order_status,
)
from app.services.auth import get_current_user
from app.models.user import User
from app.db import get_db

router = APIRouter()

@router.post("/orders")
def create(order_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_order(db, current_user.id, order_data)

@router.get("/orders/{order_id}")
def get(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/available")
def available(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_available_orders(db)

@router.post("/orders/{order_id}/accept")
def accept(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return accept_order(db, current_user.id, order_id)

@router.post("/orders/{order_id}/complete")
def complete(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return complete_order(db, current_user.id, order_id)

@router.get("/orders/me")
def mine(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_orders_for_hvac(db, current_user.id)

@router.post("/orders/{order_id}/upload-result")
def upload_result(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return upload_result_file(db, current_user.id, order_id, data.get("url"))

@router.post("/orders/{order_id}/upload-diagnostic")
def upload_diagnostic(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return upload_diagnostic_file(db, current_user.id, order_id, data.get("url"))

@router.post("/orders/{order_id}/rate")
def rate(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return rate_order(db, current_user.id, order_id, data.get("rating"))

@router.patch("/orders/{order_id}/status")
def patch_status(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_status = data.get("status")
    order = update_order_status(db, current_user.id, order_id, new_status)
    order["updated_at"] = str(datetime.utcnow())
    return order
