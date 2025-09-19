# app/api/warehouse_api.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.material import Material
from app.models.material_request import MaterialRequest
from app.models.order import Order
from app.models.user import User
from app.schemas.material import MaterialOut
from app.services.auth import get_current_user

router = APIRouter(prefix="/warehouse", tags=["warehouse"])


def check_warehouse(user: User):
    if user.role != "warehouse":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")



# 📌 ПРОФИЛЬ СКЛАДСКОГО РАБОТНИКА
@router.get("/profile")
def get_warehouse_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_warehouse(current_user)
    return {
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "organization": current_user.organization,
       
    }


@router.get("/materials", response_model=List[MaterialOut])
def get_all_materials(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_warehouse(current_user)
    return db.query(Material).all()


@router.put("/materials/{material_id}/accept")
def accept_material(material_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_warehouse(current_user)
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.stock = material.qty_received
    material.status = "accepted"
    db.commit()
    return {"detail": "Material accepted"}


@router.post("/orders/{order_id}/issue-materials")
def issue_materials_for_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_warehouse(current_user)

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    hvac_id = order.hvac_id
    if not hvac_id:
        raise HTTPException(status_code=400, detail="Order not assigned to HVAC")

    approved_requests = db.query(MaterialRequest).filter(
        MaterialRequest.order_id == order_id,
        MaterialRequest.hvac_id == hvac_id,
        MaterialRequest.approved == True,
        MaterialRequest.issued == False
    ).all()

    if not approved_requests:
        raise HTTPException(status_code=400, detail="No approved requests to issue")

    for req in approved_requests:
        material = db.query(Material).filter(Material.id == req.material_id).first()
        if not material:
            continue
        if material.stock < req.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {material.name}")
        material.stock -= req.quantity
        req.issued = True
        req.issued_date = db.execute("SELECT CURRENT_TIMESTAMP").scalar()
        req.issued_to_hvac = hvac_id
        req.qty_issued = req.quantity

    db.commit()
    return {"detail": "Materials issued to HVAC"}
