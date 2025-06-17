
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.order import Order, OrderStatus

def create_order(db: Session, client_id: int, data: dict):
    order = Order(
        client_id=client_id,
        hvac_id=data.get("hvac_id"),
        address=data.get("address"),
        lat=data.get("lat"),
        lng=data.get("lng"),
        description=data.get("description"),
        status=OrderStatus.new,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def list_available_orders(db: Session):
    return db.query(Order).filter(Order.status == OrderStatus.new).all()

def accept_order(db: Session, hvac_id: int, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or order.status != OrderStatus.new:
        return None
    order.hvac_id = hvac_id
    order.status = OrderStatus.accepted
    order.started_at = datetime.utcnow()
    db.commit()
    return order

def complete_order(db: Session, hvac_id: int, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order or order.status != OrderStatus.in_progress:
        return None
    order.status = OrderStatus.completed
    order.completed_at = datetime.utcnow()
    db.commit()
    return order

def get_orders_for_hvac(db: Session, hvac_id: int):
    return db.query(Order).filter(Order.hvac_id == hvac_id).all()

def upload_result_file(db: Session, hvac_id: int, order_id: int, url: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.result_file_url = url
    db.commit()
    return order

def upload_diagnostic_file(db: Session, hvac_id: int, order_id: int, url: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.diagnostic_file_url = url
    db.commit()
    return order

def rate_order(db: Session, hvac_id: int, order_id: int, rating: int):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.rating = rating
    db.commit()
    return order

def update_order_status(db: Session, hvac_id: int, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.status = status
    order.updated_at = datetime.utcnow()
    db.commit()
    return {
        "id": order.id,
        "status": order.status,
        "updated_at": str(order.updated_at)
    }
