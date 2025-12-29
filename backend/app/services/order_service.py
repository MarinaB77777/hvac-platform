# hvac-platform/backend/app/services/order_service.py
import json # 03.09.2025
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.order import Order, OrderStatus
from app.models.user import User 

def create_order(db: Session, client_id: int, data: dict):
    distance_cost = data.get("distance_cost")
    diagnostic_cost = data.get("diagnostic_cost", 200)  # фиксированная цена

    order = Order(
        client_id=client_id,
        hvac_id=data.get("hvac_id"),
        address=data.get("address"),
        lat=data.get("lat"),
        lng=data.get("lng"),
        description=data.get("description"),
        diagnostic_cost=diagnostic_cost,
        distance_cost=distance_cost,
        currency=data.get("currency"),
        payment_type=data.get("payment_type"),
        # ✅ НИЧЕГО ЛИШНЕГО
        client_datetime = data.get("client_datetime"),
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
    # 👉 Обновим статус мастера
    hvac = db.query(User).filter(User.id == hvac_id).first()
    if hvac:
        hvac.status = "busy"
    db.commit()
    return order

def complete_order(db: Session, hvac_id: int, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order or order.status != OrderStatus.in_progress:
        return None
    order.status = OrderStatus.completed
    order.completed_at = datetime.utcnow()

    hvac = db.query(User).filter(User.id == hvac_id).first()
    if hvac:
        hvac.status = 'free'
    db.commit()
    return order

def get_orders_for_client(db: Session, client_id: int):
    orders = db.query(Order).filter(Order.client_id == client_id).all()
    return [
        {
            "id": o.id,
            "created_at": o.created_at.isoformat() if o.created_at else None,
            "status": o.status,
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
            "rating": o.rating,
        }
        for o in orders
    ]

def get_orders_for_hvac(db: Session, hvac_id: int):
    return db.query(Order).filter(Order.hvac_id == hvac_id).all()

def upload_result_file(db: Session, hvac_id: int, order_id: int, url: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None

    order.result_file_url = url
    order.status = OrderStatus.completed
    order.completed_at = datetime.utcnow()

    hvac = db.query(User).filter(User.id == hvac_id).first()
    if hvac:
        hvac.status = "free"
           
    db.commit()
    return order

def upload_diagnostic_file(db: Session, hvac_id: int, order_id: int, url: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.diagnostic_file_url = url
    db.commit()
    return order
    
# 03.03.2025
# ✅ Добавить 1 файл в diagnostic_files[]
def add_additional_diagnostic_file(db: Session, hvac_id: int, order_id: int, url: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None

    current = json.loads(order.diagnostic_files or "[]")
    current.append(url)
    order.diagnostic_files = json.dumps(current)
    db.commit()
    return order

# ✅ Добавить 1 файл в result_files[]
def add_additional_result_file(db: Session, hvac_id: int, order_id: int, url: str):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None

    current = json.loads(order.result_files or "[]")
    current.append(url)
    order.result_files = json.dumps(current)
    db.commit()
    return order

# ✅ Сохранить список файлов диагностики (если сразу несколько)
def upload_multiple_diagnostic_files(db: Session, hvac_id: int, order_id: int, files: list):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.diagnostic_files = json.dumps(files)
    db.commit()
    return order

# ✅ Сохранить список итоговых файлов (если сразу несколько)
def upload_multiple_result_files(db: Session, hvac_id: int, order_id: int, files: list):
    order = db.query(Order).filter(Order.id == order_id, Order.hvac_id == hvac_id).first()
    if not order:
        return None
    order.result_files = json.dumps(files)
    db.commit()
    return order
# _______

def rate_order(db: Session, client_id: int, order_id: int, rating: int):
    order = db.query(Order).filter(Order.id == order_id, Order.client_id == client_id).first()
    if not order or order.rating is not None:
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
