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
import shutil

router = APIRouter()

# Проверка и установка пути к tesseract
tesseract_path = shutil.which("tesseract")
print(f"🔍 Проверка tesseract path: {tesseract_path}")
if not tesseract_path:
    print("❗️tesseract не найден в PATH, указываем вручную")
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:
    print(f"✅ tesseract найден: {tesseract_path}")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

print(f"✅ Используется tesseract: {pytesseract.pytesseract.tesseract_cmd}")

@router.post("/warehouse/recognize-image")
async def recognize_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        # Чтение файла
        filename = image.filename
        contents = await image.read()
        print(f"📸 Получено изображение: {filename}")

        # Открытие и преобразование
        pil_image = Image.open(BytesIO(contents)).convert("RGB")
        print(f"📸 Размер изображения: {pil_image.size}, формат: {pil_image.format}")
        print(f"🔧 Запускаем OCR с командой: {pytesseract.pytesseract.tesseract_cmd}")

        # Распознавание
        try:
            text = pytesseract.image_to_string(pil_image)
            print("📄 Результат OCR:")
            print(text)
        except Exception as e:
            print(f"🔥 Ошибка Tesseract: {e}")
            raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")

        # Поиск нужных полей
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

        # Финальный результат
        material = {
            "name": "Распознанный материал",
            "model": model,
            "brand": brand,
            "specs": f"PNC: {pnc}, SN: {serial}",
            "price_usd": None,
            "price_mxn": None,
            "arrival_date": datetime.utcnow().date().isoformat(),  # ⏱ текущая дата
            "stock": None,  # вручную
            "qty_issued": 0,
            "status": "pending",
            "photo_url": f"/media/{filename}",  # заглушка (или путь в хранилище)
        }

        print("✅ Распознанные данные:", material)
        return JSONResponse(content=material)

    except Exception as e:
        print(f"🔥 Общая ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")
