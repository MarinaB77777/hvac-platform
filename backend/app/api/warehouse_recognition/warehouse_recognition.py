# backend/app/api/warehouse_recognition.py

import os
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.material import Material
from app.services.auth import get_current_user
import pytesseract
from PIL import Image
from io import BytesIO
import logging

router = APIRouter()

# Установка пути к Tesseract (для Render или других окружений)
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
print(f"✅ Используется tesseract: {pytesseract.pytesseract.tesseract_cmd}")

@router.post("/warehouse/recognize-image")
async def recognize_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        # Проверка файла
        filename = image.filename
        contents = await image.read()
        print(f"📸 Получено изображение: {filename}")

        # Преобразуем в RGB и читаем
        pil_image = Image.open(BytesIO(contents)).convert("RGB")

        # Распознавание
        try:
            text = pytesseract.image_to_string(pil_image)
        except Exception as e:
            print(f"🔥 Ошибка Tesseract: {e}")
            raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")

        # Фильтрация
        def extract_field(label):
            for line in text.splitlines():
                if label.lower() in line.lower():
                    return line.split(":")[-1].strip()
            return None

        model = extract_field("model")
        brand = extract_field("brand")
        pnc = extract_field("pnc")
        serial = extract_field("serial")

        if not any([model, brand, pnc, serial]):
            print("⚠️ Ни одно из нужных полей не найдено.")
            raise HTTPException(status_code=422, detail="Не удалось найти нужные поля")

        # Формирование объекта
        material = {
            "name": "Распознанный материал",
            "model": model,
            "brand": brand,
            "specs": f"PNC: {pnc}, SN: {serial}",
            "price_usd": None,
            "price_mxn": None,
            "arrival_date": datetime.utcnow().date().isoformat(),
            "stock": None,
            "qty_issued": 0,
            "status": "pending",
            "photo_url": f"/media/{filename}",  # путь в зависимости от хранилища
        }

        print("✅ Распознанные данные:", material)
        return JSONResponse(content=material)

    except Exception as e:
        print(f"🔥 Общая ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")
