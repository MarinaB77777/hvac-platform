from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.material_request import MaterialRequest
from app.services.auth import get_current_user

router = APIRouter()

# 📦 Получить список всех заявок на материалы
@router.get("/material-requests/")
def list_requests(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can view all requests")
    return db.query(MaterialRequest).all()


# ✅ Подтвердить заявку на материал
@router.post("/material-requests/{req_id}/confirm")
def confirm_request(req_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can confirm requests")
    request = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = "confirmed"
    db.commit()
    db.refresh(request)
    return request


# 📦 Выдать заявку на материал
@router.post("/material-requests/{req_id}/issue")
def issue_request(req_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Only warehouse can issue materials")
    request = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    if request.status != "confirmed":
        raise HTTPException(status_code=400, detail="Request must be confirmed first")
    request.status = "issued"
    db.commit()
    db.refresh(request)
    return request
