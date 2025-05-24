from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db
from app.services.auth import get_current_user
from app.models.order import Order
from app.models.material_request import MaterialRequest

router = APIRouter()

@router.get("/analytics/hvac")
def hvac_analytics(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only manager can view HVAC analytics")

    orders = db.query(Order).all()
    summary = {}

    for order in orders:
        if not order.hvac_id:
            continue
        uid = order.hvac_id
        if uid not in summary:
            summary[uid] = {
                "orders": 0,
                "declined": 0,
                "total_duration": 0,
                "completed": 0,
                "materials_cost": 0
            }
        summary[uid]["orders"] += 1
        if order.status == "declined":
            summary[uid]["declined"] += 1
        if order.status == "completed" and order.started_at and order.completed_at:
            duration = (order.completed_at - order.started_at).total_seconds()
            summary[uid]["total_duration"] += duration
            summary[uid]["completed"] += 1
        if hasattr(order, "materials_cost") and order.materials_cost:
            summary[uid]["materials_cost"] += order.materials_cost

    result = []
    for uid, data in summary.items():
        avg_duration = data["total_duration"] / data["completed"] if data["completed"] else 0
        result.append({
            "hvac_id": uid,
            "orders_total": data["orders"],
            "declined": data["declined"],
            "avg_duration_minutes": round(avg_duration / 60, 1),
            "materials_cost": round(data["materials_cost"], 2),
            "flags": [
                "много отказов" if data["declined"] / data["orders"] > 0.3 else "",
                "высокие расходы" if data["materials_cost"] > 300 else ""
            ]
        })

    return result

@router.get("/analytics/warehouse")
def warehouse_analytics(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only manager can view warehouse analytics")

    requests = db.query(MaterialRequest).all()
    pending = [r for r in requests if r.status == "pending"]
    confirmed = [r for r in requests if r.status == "confirmed"]
    issued = [r for r in requests if r.status == "issued"]

    return {
        "total_requests": len(requests),
        "pending": len(pending),
        "confirmed": len(confirmed),
        "issued": len(issued),
        "issues": [
            "много неподтвержденных заявок" if len(pending) > 5 else "",
            "долго не выдаются" if len(confirmed) > 5 else ""
        ]
    }
