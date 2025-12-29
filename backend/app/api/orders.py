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
from app.services.order_service import (
    add_additional_diagnostic_file,
    add_additional_result_file
)
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
    return {
    "id": order.id,
    "client_id": order.client_id,      # ✅ ВЕРНУТЬ
    "hvac_id": order.hvac_id,           # ✅ ВЕРНУТЬ
        
    "status": order.status,
    "address": order.address,
    "description": order.description,
    "lat": order.lat,
    "lng": order.lng,

    "created_at": order.created_at.isoformat() if order.created_at else None,
    "started_at": order.started_at.isoformat() if order.started_at else None,
    "completed_at": order.completed_at.isoformat() if order.completed_at else None,

    # 🔑 ВОТ ОНО
    "datetime": order.client_datetime.isoformat() if order.client_datetime else None,

    "diagnostic_cost": order.diagnostic_cost,
    "distance_cost": order.distance_cost,
    "parts_cost": order.parts_cost,
    "repair_cost": order.repair_cost,
    "agreed_total_mxn": order.agreed_total_mxn,
    "currency": order.currency,
    "payment_type": order.payment_type,
    "diagnostic_url": order.diagnostic_url,
    "diagnostic_files": order.diagnostic_files,
    "result_file_url": order.result_file_url,
    "result_files": order.result_files,
}

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

@router.get("/active-for-manager")
def active_orders_for_manager(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only managers can access this.")

    active_orders = db.query(Order).filter(Order.status != "completed").all()

    result = []
    for order in active_orders:
        client = db.query(User).filter(User.id == order.client_id).first()
        hvac_user = db.query(User).filter(User.id == order.hvac_id).first() if order.hvac_id else None

        result.append({
            "id": order.id,
            "status": order.status,
            "address": order.address,
            "description": order.description,
            "lat": order.lat,
            "lng": order.lng,
            "created_at": order.created_at,
            "client": {
                "id": client.id,
                "name": client.name,
                "location": client.location if client else None
            },
            "hvac": {
                "id": hvac_user.id,
                "name": hvac_user.name,
                "status": hvac_user.status,
                "location": hvac_user.location,
                "organization": hvac_user.organization

            } if hvac_user else None
        })

    return result

@router.get("/all-for-manager")
def all_orders_for_manager(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only managers can access this.")

    all_orders = db.query(Order).all()

    result = []
    for order in all_orders:
        client = db.query(User).filter(User.id == order.client_id).first()
        hvac_user = db.query(User).filter(User.id == order.hvac_id).first() if order.hvac_id else None

        result.append({
            "id": order.id,
            "status": order.status,
            "address": order.address,
            "description": order.description,
            "lat": order.lat,
            "lng": order.lng,
            "started_at": order.started_at,
            "completed_at": order.completed_at,
            "rating": order.rating,
            "repair_cost": order.repair_cost,
            "diagnostic_cost": order.diagnostic_cost,
            "distance_cost": order.distance_cost,
            "agreed_total_mxn": order.agreed_total_mxn,
            "total_time": str(order.completed_at - order.started_at) if order.started_at and order.completed_at else None,
            "client": {
                "id": client.id,
                "name": client.name,
                "location": client.location if client else None
            },
            "hvac": {
                "id": hvac_user.id,
                "name": hvac_user.name,
                "status": hvac_user.status,
                "location": hvac_user.location,
                "organization": hvac_user.organization
            } if hvac_user else None
        })

    return result

@router.post("/orders/{order_id}/upload-result")
def upload_result(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return upload_result_file(db, current_user.id, order_id, data.get("url"))

@router.post("/orders/{order_id}/upload-diagnostic")
def upload_diagnostic(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return upload_diagnostic_file(db, current_user.id, order_id, data.get("url"))

# 03.09.2025
@router.post("/orders/{order_id}/add-additional-diagnostic")
def add_diagnostic_file(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_additional_diagnostic_file(db, current_user.id, order_id, data.get("url"))

@router.post("/orders/{order_id}/add-additional-result")
def add_result_file(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_additional_result_file(db, current_user.id, order_id, data.get("url"))

# 09.12.2025
@router.post("/orders/{order_id}/decline")
def decline_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Только HVAC может отказаться
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC workers can decline orders.")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Заказ должен быть принят HVAC
    if order.hvac_id != current_user.id:
        raise HTTPException(status_code=400, detail="This order is not assigned to you")

    # Обновляем статус
    order.status = OrderStatus.declined
    order.hvac_id = None     # освободить заказ

    db.commit()
    db.refresh(order)

    return {"detail": "Order declined", "order": order}
# __________

@router.patch("/orders/{order_id}/status")
def patch_status(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_status = data.get("status")
    order = update_order_status(db, current_user.id, order_id, new_status)
    order["updated_at"] = str(datetime.utcnow())
    return order

@router.post("/orders/{order_id}/rate")
def rate(order_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rating = data.get("rating")
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be an integer from 1 to 5")

    result = rate_order(db, current_user.id, order_id, rating)
    if not result:
        raise HTTPException(status_code=403, detail="Unable to rate this order. It may be already rated or doesn't belong to you.")
    return {"status": "ok", "rating": rating}

@router.patch("/orders/{order_id}")
def update_order(order_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    allowed_fields = [
        "diagnostic_url", "diagnostic_cost", "distance_cost", "parts_cost",
        "repair_cost", "agreed_total_mxn", "currency", "payment_type"
    ]
    for field in allowed_fields:
        if field in data:
            setattr(order, field, data[field])

    db.commit()
    db.refresh(order)

    return {"status": "ok", "updated_order": {
        field: getattr(order, field) for field in allowed_fields
    }}

@router.get("/orders/assigned")
def assigned_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVACs can access this.")

    print(f"🛠️ HVAC #{current_user.id} запрашивает свои заказы")

    return db.query(Order).filter(
        Order.status == OrderStatus.new,
        Order.hvac_id == current_user.id
    ).all()


























