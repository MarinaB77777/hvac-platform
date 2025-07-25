from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.order_service import (
    create_order,
    get_order_by_id,
    list_available_orders,
    accept_order,
    complete_order,
    get_orders_for_hvac,
    upload_result_file,
    upload_diagnostic_file,
    rate_order,
    update_order_status
)
from app.services.auth import get_current_user
from app.models.user import User
from app.models.order import Order, OrderStatus
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

@router.get("/orders/client")
def get_orders_for_client(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can access this.")
    return db.query(Order).filter(Order.client_id == current_user.id).all()
    
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

@router.patch("/orders/{order_id}")
def update_order(order_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if "diagnostic_url" in data:
        order.diagnostic_url = data["diagnostic_url"]

    db.commit()
    db.refresh(order)
    return {"status": "ok", "diagnostic_url": order.diagnostic_url}

@router.get("/orders/assigned")
def assigned_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVACs can access this.")

    print(f"🛠️ HVAC #{current_user.id} запрашивает свои заказы")

    return db.query(Order).filter(
        Order.status == OrderStatus.new,
        Order.hvac_id == current_user.id
    ).all()
