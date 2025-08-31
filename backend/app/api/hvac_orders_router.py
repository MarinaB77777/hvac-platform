# backend/app/api/hvac_orders_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.order import Order
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/hvac", tags=["hvac"])

@router.get("/orders")
def get_orders_for_hvac(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Access denied")

    orders = db.query(Order).all()

    return [
        {
            "id": o.id,
            "created_at": o.created_at.isoformat() if o.created_at else None,
            "status": o.status,
            "client_id": o.client_id,
            "hvac_id": o.hvac_id,
            "address": o.address,
            "lat": o.lat,
            "lng": o.lng,
            "description": o.description,
            "diagnostic_cost": o.diagnostic_cost,
            "distance_cost": o.distance_cost,
            "parts_cost": o.parts_cost,
            "repair_cost": o.repair_cost,
            "currency": o.currency,
            "payment_type": o.payment_type,
            "rating": o.rating
        }
        for o in orders
    ]
