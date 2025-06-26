# backend/app/api/warehouse_recognition.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from app.services.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/warehouse/recognize-image")
async def recognize_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    filename = image.filename
    contents = await image.read()
    print(f"📸 Получено изображение: {filename} (размер: {len(contents)} байт)")

    # Здесь будет обращение к OCR микросервису
    raise HTTPException(status_code=501, detail="🔧 OCR временно недоступен")
