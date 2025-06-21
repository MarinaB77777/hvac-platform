# backend/app/api/warehouse_api.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material

router = APIRouter(prefix="/warehouse", tags=["warehouse"])

@router.get("/materials", response_class=JSONResponse)
def get_all_materials(db: Session = Depends(get_db)):
    try:
        materials = db.query(Material).all()
        serialized = jsonable_encoder(materials)
        return JSONResponse(content=serialized)
    except Exception as e:
        print("❌ Ошибка при получении материалов:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
