# app/api/materials.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/materials/")
def get_all_materials(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Material).all()
