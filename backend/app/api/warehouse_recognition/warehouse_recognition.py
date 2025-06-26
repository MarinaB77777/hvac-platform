# backend/app/api/warehouse_recognition/warehouse_recognition.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
import shutil
import os
import io
import re

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse_recognition"]
)

# 🛠 Указываем путь к tesseract, если он не в PATH
tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    print("❗️tesseract не найден в PATH, указываем вручную")
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:
    print(f"✅ tesseract найден: {tesseract_path}")

@router.post("/recognize-image")
async def recognize_image(image: UploadFile = File(...)):
    try:
        print(f"📸 Получено изображение: {image.filename}")

        contents = await image.read()

        # Открываем изображение
        try:
            pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="❌ Неподдерживаемый формат изображения")

        # Распознаём текст
        try:
            recognized_text = pytesseract.image_to_string(pil_image)
            print("🔤 Распознанный текст:", recognized_text)
        except Exception as e:
            print("🔥 Ошибка Tesseract:", e)
            raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")

        # Ищем ключевые данные
        model_match = re.search(r'MODEL[:\s]*([A-Z0-9\-]+)', recognized_text, re.IGNORECASE)
        pnc_match = re.search(r'PNC[:\s#]*([0-9\s]{6,})', recognized_text, re.IGNORECASE)
        serial_match = re.search(r'(?:Serial|S\/N|SN|SN-T)[:\s]*([A-Z0-9\- ]+)', recognized_text, re.IGNORECASE)
        brand_match = re.search(r'Electrolux|Samsung|LG|Bosch|Whirlpool|GE', recognized_text, re.IGNORECASE)

        return {
            "model": model_match.group(1).strip() if model_match else None,
            "pnc": pnc_match.group(1).strip() if pnc_match else None,
            "serial_number": serial_match.group(1).strip() if serial_match else None,
            "brand": brand_match.group(0).strip() if brand_match else None,
            "raw_text": recognized_text,
        }

    except Exception as e:
        print("🔥 Общая ошибка при распознавании:", str(e))
        raise HTTPException(status_code=500, detail="❌ Ошибка сервера при распознавании")
