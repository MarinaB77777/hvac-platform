from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.auth import get_current_user

router = APIRouter()

# Заявки на материалы
material_requests = []
request_counter = 1

@router.post("/material-requests/")
def create_request(data: dict = Body(...), user=Depends(get_current_user)):
    global request_counter
    if user["role"] != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create requests")
    req = {
        "id": request_counter,
        "hvac_id": user["id"],
        "order_id": data["order_id"],
        "name": data["name"],
        "brand": data["brand"],
        "qty": data["qty"],
        "status": "pending"
    }
    material_requests.append(req)
    request_counter += 1
    return req

@router.get("/material-requests/")
def list_requests(user=Depends(get_current_user)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse sees all requests")
    return material_requests

@router.post("/material-requests/{req_id}/confirm")
def confirm_request(req_id: int, user=Depends(get_current_user)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can confirm")
    for req in material_requests:
        if req["id"] == req_id:
            req["status"] = "confirmed"
            return req
    raise HTTPException(status_code=404, detail="Request not found")

@router.post("/material-requests/{req_id}/issue")
def issue_request(req_id: int, user=Depends(get_current_user)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can issue")
    for req in material_requests:
        if req["id"] == req_id:
            if req["status"] != "confirmed":
                raise HTTPException(status_code=400, detail="Request must be confirmed first")
            req["status"] = "issued"
            return req
    raise HTTPException(status_code=404, detail="Request not found")
