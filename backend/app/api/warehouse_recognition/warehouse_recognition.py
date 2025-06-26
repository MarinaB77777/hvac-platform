from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
import io
import re
import logging

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse_recognition"]
)

logger = logging.getLogger("uvicorn.error")

@router.post("/recognize-image")
async def recognize_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        logger.info(f"📸 Получено изображение: {image.filename}")

        try:
            pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            logger.error("❌ Неподдерживаемый формат изображения")
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат изображения")

        # Распознавание текста
        recognized_text = pytesseract.image_to_string(pil_image)
        logger.info(f"📄 Распознанный текст:\n{recognized_text}")

        # Поиск ключевых данных
        model_match = re.search(r'MODEL\s*[:\-]?\s*([A-Z0-9\-]+)', recognized_text, re.IGNORECASE)
        pnc_match = re.search(r'PNC\s*[:\-]?\s*([\d\s]+)', recognized_text, re.IGNORECASE)
        serial_match = re.search(r'SERIAL\s*NO\.?\s*[:\-]?\s*([0-9]+)', recognized_text, re.IGNORECASE)

        result = {
            "model": model_match.group(1) if model_match else None,
            "pnc": pnc_match.group(1).strip() if pnc_match else None,
            "serial": serial_match.group(1) if serial_match else None,
            "recognized_text": recognized_text,
        }

        logger.info(f"✅ Извлечённые данные: {result}")
        return result

    except Exception as e:
        logger.error(f"🔥 Ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail="Ошибка распознавания")
