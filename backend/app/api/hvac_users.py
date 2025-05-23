from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.auth import get_current_user

router = APIRouter()

hvac_users = [
    {
        "id": 2,
        "name": "Иванов Иван",
        "phone": "79001234567",
        "profile": "монтаж",
        "diagnostic_fee": 30,
        "work_fee": 70,
        "transport_fee": 0.5,
        "qualification": "средний"
    },
    {
        "id": 3,
        "name": "Петров Пётр",
        "phone": "79001112233",
        "profile": "ремонт",
        "diagnostic_fee": 35,
        "work_fee": 75,
        "transport_fee": 0.6,
        "qualification": "высокий"
    }
]

@router.get("/hvac-users/")
def list_hvac_users(user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only manager can view HVAC users")
    return hvac_users

@router.patch("/hvac-users/{user_id}")
def update_hvac_user(user_id: int, data: dict = Body(...), user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only manager can update HVAC users")

    for u in hvac_users:
        if u["id"] == user_id:
            u.update({
                "diagnostic_fee": data.get("diagnostic_fee", u["diagnostic_fee"]),
                "work_fee": data.get("work_fee", u["work_fee"]),
                "transport_fee": data.get("transport_fee", u["transport_fee"]),
                "qualification": data.get("qualification", u["qualification"]),
            })
            return u

    raise HTTPException(status_code=404, detail="User not found")
