from fastapi import APIRouter, Depends
from app.services.auth import get_current_user
from datetime import datetime
from app.api.order import orders
from app.api.hvac_materials import hvac_materials
from app.api.warehouse import material_requests

router = APIRouter()

@router.get("/analytics/hvac")
def hvac_analytics(user=Depends(get_current_user)):
    if user["role"] != "manager":
        return {"error": "Only manager can view HVAC analytics"}

    summary = {}
    for order in orders:
        if not order["hvac_id"]:
            continue
        uid = order["hvac_id"]
        if uid not in summary:
            summary[uid] = {
                "orders": 0,
                "declined": 0,
                "total_duration": 0,
                "completed": 0,
                "materials_cost": 0
            }
        summary[uid]["orders"] += 1
        if order["status"] == "declined":
            summary[uid]["declined"] += 1
        if order["status"] == "completed" and order.get("started_at") and order.get("completed_at"):
            start = datetime.fromisoformat(order["started_at"])
            end = datetime.fromisoformat(order["completed_at"])
            summary[uid]["total_duration"] += (end - start).total_seconds()
            summary[uid]["completed"] += 1
        if order.get("materials_cost"):
            summary[uid]["materials_cost"] += order["materials_cost"]

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
def warehouse_analytics(user=Depends(get_current_user)):
    if user["role"] != "manager":
        return {"error": "Only manager can view warehouse analytics"}

    pending = [r for r in material_requests if r["status"] == "pending"]
    confirmed = [r for r in material_requests if r["status"] == "confirmed"]
    issued = [r for r in material_requests if r["status"] == "issued"]

    return {
        "total_requests": len(material_requests),
        "pending": len(pending),
        "confirmed": len(confirmed),
        "issued": len(issued),
        "issues": [
            "много неподтвержденных заявок" if len(pending) > 5 else "",
            "долго не выдаются" if len(confirmed) > 5 else ""
        ]
    }
