# hvac_orders.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.schemas.order import OrderOut  # если у тебя есть сериализатор
from typing import List

router = APIRouter(prefix="/hvac/orders", tags=["hvac-orders"])

@router.get("/available", response_model=List[OrderOut])
def get_all_available_orders_for_hvac(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "hvac":
        raise HTTPException(status_code=403, detail="Только для HVAC")

    orders = db.query(Order).filter(Order.status == OrderStatus.new).all()
    return orders
