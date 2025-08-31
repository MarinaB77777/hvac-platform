# backend/app/api/hvac_orders_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.models.order import Order
from app.services.auth import get_current_user

router = APIRouter(prefix="/hvac", tags=["hvac"])

# 📍 Получить все заказы для HVAC
@router.get("/orders")
def get_all_orders_for_hvac(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Access denied")

    orders = db.query(Order).all()

    return [
        {
            "id": order.id,
            "address": order.address,
            "lat": order.lat,
            "lng": order.lng,
            "description": order.description,
            "status": order.status,
            "datetime": order.datetime,
            "hvac_id": order.hvac_id,
        }
        for order in orders
    ]
