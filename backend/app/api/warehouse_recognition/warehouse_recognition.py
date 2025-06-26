# backend/app/api/warehouse_recognition/warehouse_recognition.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
import os
import io
import re
import shutil
from datetime import datetime

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse_recognition"]
)

# 🔍 Проверка и установка пути к tesseract
tesseract_path = shutil.which("tesseract") or os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")

if not tesseract_path:
    raise RuntimeError("❌ Tesseract не найден ни в PATH, ни через переменную окружения TESSERACT_CMD")

pytesseract.pytesseract.tesseract_cmd = tesseract_path
print(f"✅ Используется tesseract: {tesseract_path}")

@router.post("/recognize-image")
async def recognize_image(image: UploadFile = File(...)):
    try:
        print(f"📸 Получено изображение: {image.filename}")
        contents = await image.read()

        # 🔍 Пробуем открыть изображение
        try:
            pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="❌ Неподдерживаемый формат изображения")

        # 🧠 Распознаём текст
        try:
            recognized_text = pytesseract.image_to_string(pil_image)
            print(f"🧾 Распознанный текст:\n{recognized_text}")
        except Exception as e:
            print(f"🔥 Ошибка Tesseract: {str(e)}")
            raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")

        # 🔍 Поиск ключевых полей
        model_match = re.search(r'MODEL\s*[:\-]?\s*([\w\-\/]+)', recognized_text, re.IGNORECASE)
        pnc_match = re.search(r'PNC\s*[:\-]?\s*([\w\-]+)', recognized_text, re.IGNORECASE)
        serial_match = re.search(r'SERIAL\s*NO\s*[:\-]?\s*([\w\-]+)', recognized_text, re.IGNORECASE)

        data = {
            "model": model_match.group(1) if model_match else None,
            "pnc": pnc_match.group(1) if pnc_match else None,
            "serial": serial_match.group(1) if serial_match else None,
            "status": "pending",
            "recognized_at": datetime.utcnow().isoformat()
        }

        print(f"📦 Извлечённые данные: {data}")
        return JSONResponse(content=data)

    except Exception as e:
        print(f"🔥 Общая ошибка при распознавании: {str(e)}")
        raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")
