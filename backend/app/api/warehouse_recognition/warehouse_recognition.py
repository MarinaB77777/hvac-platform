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
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import logging
import easyocr

router = APIRouter()

# 🔧 Инициализация EasyOCR
reader = easyocr.Reader(['en'], gpu=False)
print("✅ EasyOCR инициализирован")

@router.post("/warehouse/recognize-image")
async def recognize_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        filename = image.filename
        contents = await image.read()
        print(f"📸 Получено изображение: {filename}")

        try:
            pil_image = Image.open(BytesIO(contents)).convert("RGB")
            print(f"📸 Размер изображения: {pil_image.size}, формат: {pil_image.format}")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="❌ Неподдерживаемый формат изображения")

        # Конвертация в numpy массив для EasyOCR
        import numpy as np
        np_image = np.array(pil_image)

        print("🔧 Запускаем EasyOCR...")
        results = reader.readtext(np_image, detail=0)
        full_text = "\n".join(results)
        print("📄 Распознанный текст:\n", full_text)

        def extract_field(label):
            for line in results:
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
            "photo_url": f"/media/{filename}",
        }

        print("✅ Распознанные данные:", material)
        return JSONResponse(content=material)

    except Exception as e:
        print(f"🔥 Общая ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")
