from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import get_current_user  # поправь, если у вас другое имя
from app.models.order import Order, OrderStatus  # поправь путь к модели

router = APIRouter(prefix="/free-orders", tags=["Free Orders"])


def _ensure_hvac_user(user):
    # если у вас есть role-поле — можно включить проверку тут
    return


@router.get("")
def list_free_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    _ensure_hvac_user(user)

    orders = (
        db.query(Order)
        .filter(Order.status == OrderStatus.new)
        .filter(Order.hvac_id.is_(None))
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders


@router.get("/{order_id}")
def get_free_order(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    _ensure_hvac_user(user)

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .filter(Order.status == OrderStatus.new)
        .filter(Order.hvac_id.is_(None))
        .first()
    )
    if not order:
        raise HTTPException(404, "Free order not found")
    return order


@router.post("/{order_id}/accept")
def accept_free_order(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    _ensure_hvac_user(user)

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .filter(Order.status == OrderStatus.new)
        .filter(Order.hvac_id.is_(None))
        .with_for_update()
        .first()
    )
    if not order:
        raise HTTPException(409, "Order is no longer available")

    order.hvac_id = user.id
    order.status = OrderStatus.accepted

    db.commit()
    db.refresh(order)
    return {"status": "accepted", "order_id": order.id}


@router.post("/{order_id}/release")
def release_order_back_to_pool(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    _ensure_hvac_user(user)

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")

    if order.hvac_id != user.id:
        raise HTTPException(403, "Not your order")

    # важное правило: отпускать назад можно только если заказ ещё не в работе
    if order.status != OrderStatus.accepted:
        raise HTTPException(409, "Only accepted orders can be released")

    order.hvac_id = None
    order.status = OrderStatus.new

    db.commit()
    db.refresh(order)
    return {"status": "released", "order_id": order.id}
