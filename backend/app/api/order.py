from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.auth import get_current_user
from app.models.user import UserRole
from datetime import datetime

router = APIRouter()

# FAKE DB MOCK
orders = []
order_id_counter = 1

@router.post("/orders/")
def create_order(data: dict, user=Depends(get_current_user)):
    global order_id_counter
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can create orders")
    order = {
        "id": order_id_counter,
        "client_id": user["id"],
        "hvac_id": None,
        "status": "new",
        "address": data["address"],
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "description": data.get("description"),
        "created_at": str(datetime.utcnow()),
        "updated_at": str(datetime.utcnow()),
        "diagnostic_fee": 30,
        "work_fee": None,
        "materials_cost": None,
        "price_total": None,
        "diagnostic_file_url": None,
        "result_file_url": None,
        "rating": None,
        "diagnostic_file_url": None,
        "result_file_url": None
    }
    orders.append(order)
    order_id_counter += 1
    return order

@router.get("/orders/available")
def get_available_orders(user=Depends(get_current_user)):
    if user["role"] != "hvac":
        raise HTTPException(status_code=403, detail="Only HVACs see available orders")
    return [o for o in orders if o["status"] == "new"]

@router.post("/orders/{order_id}/take")
def take_order(order_id: int, user=Depends(get_current_user)):
    for order in orders:
        if order["id"] == order_id and order["status"] == "new":
            order["status"] = "accepted"
            order["started_at"] = str(datetime.utcnow())
            order["hvac_id"] = user["id"]
            order["updated_at"] = str(datetime.utcnow())
            return order
    raise HTTPException(status_code=404, detail="Order not found or already taken")

@router.get("/orders/me")
def my_orders(user=Depends(get_current_user)):
    if user["role"] == "client":
        return [o for o in orders if o["client_id"] == user["id"]]
    if user["role"] == "hvac":
        return [o for o in orders if o["hvac_id"] == user["id"]]
    return []

@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, user=Depends(get_current_user)):
    for order in orders:
        if order["id"] == order_id:
            if user["id"] in [order["client_id"], order["hvac_id"]]:
                order["status"] = "declined"
                order["updated_at"] = str(datetime.utcnow())
                return order
    raise HTTPException(status_code=403, detail="Not allowed to cancel this order")

from fastapi import Body

@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: dict = Body(...), user=Depends(get_current_user)):
    new_status = status.get("status")
    if new_status not in ["in_progress", "completed", "declined"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    for order in orders:
        if order["id"] == order_id:
            if user["role"] != "hvac" or order["hvac_id"] != user["id"]:
                raise HTTPException(status_code=403, detail="Not your order")

            current = order["status"]

    if current == "accepted" and new_status == "in_progress":
        order["status"] = "in_progress"
    elif current == "in_progress" and new_status == "completed":
        order["status"] = "completed"
        order["completed_at"] = str(datetime.utcnow())
    elif new_status == "declined":
        order["status"] = "declined"
        order["completed_at"] = str(datetime.utcnow())
    else:
        raise HTTPException(status_code=400, detail="Invalid status transition")


            order["updated_at"] = str(datetime.utcnow())
            return order

    raise HTTPException(status_code=404, detail="Order not found")

@router.post("/orders/{order_id}/calculate")
def calculate_order(order_id: int, payload: dict = Body(...), user=Depends(get_current_user)):
    if user["role"] != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can calculate order cost")

    for order in orders:
        if order["id"] == order_id and order["hvac_id"] == user["id"]:
            # Mock тариф работы (в реальности — из профиля HVAC)
            work_fee = 70
            materials = payload.get("materials", [])
            materials_cost = sum(m["qty"] * m["unit_price"] for m in materials)

            order["work_fee"] = work_fee
            order["materials_cost"] = materials_cost
            order["price_total"] = work_fee + materials_cost
            order["updated_at"] = str(datetime.utcnow())
            return {
                "work_fee": work_fee,
                "materials_cost": materials_cost,
                "price_total": work_fee + materials_cost
            }

    raise HTTPException(status_code=404, detail="Order not found or not yours")

@router.post("/orders/{order_id}/upload-diagnostic")
def upload_diagnostic(order_id: int, data: dict = Body(...), user=Depends(get_current_user)):
    for order in orders:
        if order["id"] == order_id and order["hvac_id"] == user["id"]:
            order["diagnostic_file_url"] = data["url"]
            return {"message": "Diagnostic uploaded", "url": data["url"]}
    raise HTTPException(status_code=404, detail="Order not found or not yours")

@router.post("/orders/{order_id}/upload-result")
def upload_result(order_id: int, data: dict = Body(...), user=Depends(get_current_user)):
    for order in orders:
        if order["id"] == order_id and order["hvac_id"] == user["id"]:
            order["result_file_url"] = data["url"]
            return {"message": "Result uploaded", "url": data["url"]}
    raise HTTPException(status_code=404, detail="Order not found or not yours")

@router.post("/orders/{order_id}/rate")
def rate_order(order_id: int, data: dict = Body(...), user=Depends(get_current_user)):
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can rate")
    rating = data.get("rating")
    if not 1 <= rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be 1 to 5")

    for order in orders:
        if order["id"] == order_id and order["client_id"] == user["id"]:
            if order.get("rating"):
                raise HTTPException(status_code=400, detail="Already rated")
            order["rating"] = rating
            return {"message": "Rating submitted"}
    raise HTTPException(status_code=404, detail="Order not found")
