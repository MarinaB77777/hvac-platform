from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material_request import MaterialRequest
from app.services.auth import get_current_user

router = APIRouter()

# 📦 Получить все заявки на материалы (только для склада)
@router.get("/material-requests/")
def get_all_requests(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Access denied: warehouse only")
    return db.query(MaterialRequest).all()


# ✅ Подтвердить заявку (warehouse)
@router.post("/material-requests/{request_id}/confirm")
def confirm_request(request_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Access denied: warehouse only")

    request = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = "confirmed"
    db.commit()
    db.refresh(request)
    return request


# 🚚 Выдать заявку (warehouse)
@router.post("/material-requests/{request_id}/issue")
def issue_request(request_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "warehouse":
        raise HTTPException(status_code=403, detail="Access denied: warehouse only")

    request = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status != "confirmed":
        raise HTTPException(status_code=400, detail="Request must be confirmed before issuing")

    request.status = "issued"
    db.commit()
    db.refresh(request)
    return request
