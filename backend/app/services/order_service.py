from sqlalchemy.orm import Session
from datetime import datetime
from app.models.order import Order, OrderStatus
from app.models.user import User  # нужно для получения координат HVAC
from math import radians, cos, sin, sqrt, atan2

# Вспомогательная функция для расчёта расстояния между двумя точками
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли в км
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def create_order(db: Session, client_id: int, data: dict):
    hvac_id = data.get("hvac_id")
    hvac = db.query(User).filter(User.id == hvac_id).first()

    lat = data.get("lat")
    lng = data.get("lng")

    # Автоматический расчёт стоимости дороги
    if hvac and lat is not None and lng is not None:
        try:
            distance_km = haversine(lat, lng, hvac.latitude, hvac.longitude)
            rate_per_km = hvac.qualification or 25
            distance_cost = int(distance_km * rate_per_km)
        except Exception:
            distance_cost = data.get("distance_cost")  # fallback
    else:
        distance_cost = data.get("distance_cost")

    # Фиксированная цена диагностики
    diagnostic_cost = data.get("diagnostic_cost", 500)

    order = Order(
        client_id=client_id,
        hvac_id=hvac_id,
        address=data.get("address"),
        lat=lat,
        lng=lng,
        description=data.get("description"),
        diagnostic_cost=diagnostic_cost,
        distance_cost=distance_cost,
        currency=data.get("currency"),
        payment_type=data.get("payment_type"),
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


def get_orders_for_client(db: Session, client_id: int):
    return db.query(Order).filter(Order.client_id == client_id).all()


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
