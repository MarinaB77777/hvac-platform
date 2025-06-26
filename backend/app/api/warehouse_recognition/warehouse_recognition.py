# backend/app/api/warehouse_recognition/warehouse_recognition.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
import io
import re
import shutil

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse_recognition"]
)

# 🔍 Проверка наличия tesseract
tesseract_path = shutil.which("tesseract")
print(f"🔍 Проверка tesseract_path: {tesseract_path}")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print(f"✅ Установлен путь к Tesseract: {tesseract_path}")
else:
    manual_path = "/usr/bin/tesseract"
    pytesseract.pytesseract.tesseract_cmd = manual_path
    print(f"⚠️ Tesseract не найден автоматически. Пробуем вручную: {manual_path}")

@router.post("/recognize-image")
async def recognize_image(image: UploadFile = File(...)):
    try:
        print(f"📸 Получено изображение: {image.filename}")
        contents = await image.read()

        # 🖼 Преобразование в RGB
        try:
            pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="❌ Неподдерживаемый формат изображения")

        # 🧠 Распознавание текста
        try:
            recognized_text = pytesseract.image_to_string(pil_image)
            print(f"📝 Распознанный текст:\n{recognized_text}")
        except Exception as e:
            print(f"🔥 Ошибка Tesseract: {e}")
            raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании текста")

        # 🔍 Извлечение данных
        model_match = re.search(r'MODEL\s*[:\-]?\s*([A-Z0-9\-]+)', recognized_text, re.IGNORECASE)
        brand_match = re.search(r'(?i)(electrolux|samsung|lg|bosch|siemens)', recognized_text)
        pnc_match = re.search(r'PNC\s*[:\-]?\s*([\d\s]+)', recognized_text, re.IGNORECASE)
        serial_match = re.search(r'SERIAL\s*[:\-]?\s*(\S+)', recognized_text, re.IGNORECASE)

        result = {
            "brand": brand_match.group(1).capitalize() if brand_match else None,
            "model": model_match.group(1) if model_match else None,
            "pnc": pnc_match.group(1).replace(" ", "") if pnc_match else None,
            "serial": serial_match.group(1) if serial_match else None,
        }

        print(f"✅ Извлечённые данные: {result}")
        return JSONResponse(content=result)

    except Exception as e:
        print(f"🔥 Общая ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail="❌ Ошибка при распознавании изображения")
