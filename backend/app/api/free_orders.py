from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.db import get_db
from app.models.order import Order, OrderStatus
from app.services.auth import get_current_user

router = APIRouter(prefix="/free-orders", tags=["Free Orders"])


def require_hvac(user):
    # подстрой под вашу модель: user.role == "hvac" или Enum
    if getattr(user, "role", None) != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can access this endpoint")


@router.get("/")
def list_free_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_hvac(user)

    orders = (
        db.query(Order)
        .filter(
            Order.hvac_id.is_(None),
            or_(Order.status == OrderStatus.new, Order.status == OrderStatus.declined),
        )
        .order_by(Order.created_at.desc())
        .all()
    )

    # можно отдавать целиком, но лучше минимум для карты:
    return [
        {
            "id": o.id,
            "status": o.status,
            "address": o.address,
            "lat": o.lat,
            "lng": o.lng,
            "description": o.description,
            "client_datetime": o.client_datetime,
            "created_at": o.created_at,
        }
        for o in orders
    ]


@router.post("/{order_id}/accept")
def accept_free_order(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_hvac(user)

    # ⚠️ важный момент: защищаемся от гонки (два HVAC нажали "Accept" одновременно)
    # В PostgreSQL можно сделать with_for_update()
    q = db.query(Order).filter(Order.id == order_id).with_for_update()
    order = q.first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.hvac_id is not None:
        raise HTTPException(status_code=409, detail="Order already taken")

    if order.status not in (OrderStatus.new, OrderStatus.declined):
        raise HTTPException(status_code=409, detail=f"Order not available (status={order.status})")

    order.hvac_id = int(user.id)
    order.status = OrderStatus.accepted
    order.started_at = order.started_at or datetime.utcnow()

    db.commit()
    db.refresh(order)

    return {"status": "accepted", "order_id": order.id, "hvac_id": order.hvac_id}
