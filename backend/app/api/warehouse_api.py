# app/api/warehouse_api.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.material import Material
from app.schemas.material import MaterialOut

router = APIRouter()

# 🔹 Получить все материалы со склада
@router.get("/materials", response_model=List[MaterialOut])
def get_all_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()
