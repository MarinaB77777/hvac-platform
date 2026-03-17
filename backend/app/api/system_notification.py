from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.db import get_db
from app.services.auth import get_current_user
from app.models.order import Order
from app.models.system_notification import SystemNotification
from app.schemas.system_notification import (
    SystemNotificationCreate,
    SystemNotificationOut
)

router = APIRouter(prefix="/system-notifications", tags=["System Notifications"])


@router.post("/order-cancelled-by-hvac")
def notify_order_cancelled_by_hvac(
    data: SystemNotificationCreate,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    notification = SystemNotification(
        user_id=order.client_id,
        order_id=order.id,
        type="order_cancelled_by_hvac",
        title="Order cancelled",
        body="Your order was cancelled by the HVAC technician. Please choose another technician or create a free order.",
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {"status": "notification_sent", "notification_id": notification.id}


@router.get("/me", response_model=List[SystemNotificationOut])
def get_my_notifications(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(SystemNotification)
        .filter(SystemNotification.user_id == current_user.id)
        .order_by(SystemNotification.created_at.desc())
        .all()
    )
@router.post("/client-agreed")
def notify_client_agreed(
    data: SystemNotificationCreate,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    notification = SystemNotification(
        user_id=order.client_id,
        order_id=order.id,
        type="client_agreed",
        title="Agreement recorded",
        body="Your agreement to the repair amount has been recorded.",
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {"status": "notification_sent", "notification_id": notification.id}

@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notif = (
        db.query(SystemNotification)
        .filter(
            SystemNotification.id == notification_id,
            SystemNotification.user_id == current_user.id
        )
        .first()
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.read_at = datetime.utcnow()
    db.commit()

    return {"status": "ok"}
