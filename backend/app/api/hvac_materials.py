from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.auth import get_current_user

router = APIRouter(prefix="/my-materials", tags=["hvac-materials"])

# 🔹 Mock список выданных материалов
hvac_materials = [
    {
        "hvac_id": 2,
        "order_id": 42,
        "name": "Фреон",
        "brand": "R410",
        "qty": 2,
        "used": 0
    },
    {
        "hvac_id": 2,
        "order_id": 43,
        "name": "Фильтр",
        "brand": "Panasonic",
        "qty": 1,
        "used": 0
    }
]

# 🔹 Получить список выданных материалов для текущего HVAC
@router.post("/")
def get_my_materials(user=Depends(get_current_user)):
    if user["role"] != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC has materials")
    return [m for m in hvac_materials if m["hvac_id"] == user["id"]]

# 🔹 Обновить использование конкретного материала (по заказу)
@router.post("/use")
def use_material(data: dict = Body(...), user=Depends(get_current_user)):
    if user["role"] != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can update usage")

    for m in hvac_materials:
        if (
            m["hvac_id"] == user["id"]
            and m["order_id"] == data["order_id"]
            and m["name"] == data["name"]
        ):
            if data["used"] > m["qty"]:
                raise HTTPException(status_code=400, detail="Cannot use more than available")
            m["used"] = data["used"]
            return {"message": "Usage updated", "material": m}

    raise HTTPException(status_code=404, detail="Material not found")
