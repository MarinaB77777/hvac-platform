from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.db import get_db
from app.models.order import Order, OrderStatus
from app.services.auth import get_current_user
from app.schemas.free_order import FreeOrderCreate
from app.models.multiservice import MultiService
from app.models.user import User
import math

router = APIRouter(prefix="/free-orders", tags=["Free Orders"])


def require_hvac(user):
    # подстрой под вашу модель: user.role == "hvac" или Enum
    if getattr(user, "role", None) != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can access this endpoint")
def calc_distance_km(lat1, lon1, lat2, lon2):
    R = 6371

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

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

@router.post("/")
def create_free_order(
    payload: FreeOrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    order = Order(
        client_id=int(user.id),
        hvac_id=None,
        status=OrderStatus.new,
        address=payload.address,
        lat=payload.lat,
        lng=payload.lng,
        description=payload.description,
        payment_type=payload.payment_type,
        currency=payload.currency or "USD",
        client_datetime=payload.client_datetime,
        diagnostic_cost=None,
        distance_cost=None,
        parts_cost=None,
        repair_cost=None,
        agreed_total_mxn=None,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "id": order.id,
        "status": order.status,
        "client_id": order.client_id,
        "hvac_id": order.hvac_id,
        "address": order.address,
        "lat": order.lat,
        "lng": order.lng,
        "description": order.description,
        "payment_type": order.payment_type,
        "currency": order.currency,
        "client_datetime": order.client_datetime,
        "created_at": order.created_at,
    }

@router.post("/{order_id}/accept")
def accept_free_order(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_hvac(user)

    q = db.query(Order).filter(Order.id == order_id).with_for_update()
    order = q.first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.hvac_id is not None:
        raise HTTPException(status_code=409, detail="Order already taken")

    if order.status not in (OrderStatus.new, OrderStatus.declined):
        raise HTTPException(status_code=409, detail=f"Order not available (status={order.status})")

    # назначаем HVAC
    order.hvac_id = int(user.id)
    order.status = OrderStatus.accepted
    order.started_at = order.started_at or datetime.utcnow()

    # ----------------------------
    # диагностическая стоимость
    # ----------------------------

    ms = (
        db.query(MultiService)
        .filter(
            MultiService.created_by_user_id == user.id,
            MultiService.title == "HVAC",
        )
        .first()
    )

    diagnostic_cost = ms.diagnostic_price if ms else 200

    # ----------------------------
    # стоимость дороги
    # ----------------------------

    distance_cost = 0

    try:
        if user.location and order.lat and order.lng:
            hvac_lat, hvac_lng = map(float, user.location.split(","))

            distance_km = calc_distance_km(
                hvac_lat,
                hvac_lng,
                order.lat,
                order.lng,
            )

            distance_cost = round(distance_km * float(user.tarif or 0))

    except Exception as e:
        print("distance calculation error:", e)

    order.diagnostic_cost = diagnostic_cost
    order.distance_cost = distance_cost
    order.currency = "USD"

    db.commit()
    db.refresh(order)

    return {
        "status": "accepted",
        "order_id": order.id,
        "hvac_id": order.hvac_id,
        "diagnostic_cost": order.diagnostic_cost,
        "distance_cost": order.distance_cost,
    }
