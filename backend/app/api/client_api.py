from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.order import Order
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/client")

@router.get("/orders")
def get_orders_for_client(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can access this.")
    return db.query(Order).filter(Order.client_id == current_user.id).all()
    
# 15.09.2025

@router.get("/employees")
def get_hvac_for_client(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can access this.")

    hvacs = (
        db.query(User)
        .filter(
            User.role == "hvac",
            User.location.isnot(None)
        )
        .all()
    )

    result = []

    for hvac in hvacs:
        ratings = (
            db.query(Order.rating)
            .filter(
                Order.hvac_id == hvac.id,
                Order.rating.isnot(None)
            )
            .all()
        )

        avg_rating = (
            sum(r[0] for r in ratings) / len(ratings)
            if ratings else None
        )

        result.append({
            "id": hvac.id,
            "name": hvac.name,
            "location": hvac.location,
            "status": hvac.status,
            "tarif": hvac.tarif,
            "avgRating": avg_rating,
        })

    return result
