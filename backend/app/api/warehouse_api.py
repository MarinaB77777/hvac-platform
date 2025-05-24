from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.auth import get_current_user
from app.models.material_request import MaterialRequest

router = APIRouter()

@router.post("/material-requests/")
def create_request(data: dict = Body(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create requests")

    req = MaterialRequest(
        hvac_id=user["id"],
        order_id=data["order_id"],
        name=data["name"],
        brand=data.get("brand"),
        qty=data["qty"],
        status="pending"
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@router.get("/material-requests/")
def list_requests(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse sees all requests")
    return db.query(MaterialRequest).all()

@router.post("/material-requests/{req_id}/confirm")
def confirm_request(req_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can confirm")
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = "confirmed"
    db.commit()
    return req

@router.post("/material-requests/{req_id}/issue")
def issue_request(req_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can issue")
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.status != "confirmed":
        raise HTTPException(status_code=400, detail="Request must be confirmed first")
    req.status = "issued"
    db.commit()
    return req
