from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.order import Order
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/hvac")

@router.post("/orders")
def get_orders_for_hvac(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC users can access this.")

    return db.query(Order).filter(Order.hvac_id == current_user.id).all()
