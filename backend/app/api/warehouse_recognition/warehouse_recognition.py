# backend/app/api/warehouse_recognition/warehouse_recognition.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
from io import BytesIO
import re

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse_recognition"]
)

@router.post("/recognize-image")
async def recognize_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()

        # 🖼 Открываем изображение
        try:
            pil_image = Image.open(BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат изображения")

        # 🔠 Распознаём текст
        recognized_text = pytesseract.image_to_string(pil_image)

        # 🔍 Пытаемся найти ключевые поля
        model_match = re.search(r'MODEL[:\s]*([A-Z0-9\-]+)', recognized_text, re.IGNORECASE)
        pnc_match = re.search(r'PNC[:\s]*([\d\s]+)', recognized_text, re.IGNORECASE)
        serial_match = re.search(r'SERIAL\s*NO\.?[:\s]*([\d\s]+)', recognized_text, re.IGNORECASE)
        brand_match = re.search(r'Electrolux|Samsung|LG|Bosch|Whirlpool', recognized_text, re.IGNORECASE)

        material_data = {
            "brand": brand_match.group(0).strip() if brand_match else "Неизвестно",
            "model": model_match.group(1).strip() if model_match else "Неизвестно",
            "pnc": pnc_match.group(1).strip().replace(" ", "") if pnc_match else "Неизвестно",
            "serial_number": serial_match.group(1).strip().replace(" ", "") if serial_match else "Неизвестно",
            "raw_text": recognized_text
        }

        return JSONResponse(content={"status": "ok", "data": material_data})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {str(e)}")
