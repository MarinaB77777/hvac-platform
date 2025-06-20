# app/api/materials.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/materials/")
def get_all_materials(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] not in ["warehouse", "hvac", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(Material).all()
