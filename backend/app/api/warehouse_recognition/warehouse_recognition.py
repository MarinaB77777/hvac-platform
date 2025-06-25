# backend/app/api/warehouse_recognition/warehouse_recognition.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
from io import BytesIO

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse_recognition"]
)

@router.post("/recognize-image")
async def recognize_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()

        # Открываем изображение через Pillow
        image = Image.open(BytesIO(contents))

        # Распознаём текст
        recognized_text = pytesseract.image_to_string(image)

        # Простой пример разбора результата
        material_data = {
            "name": "Неизвестно",
            "brand": "Неизвестно",
            "model": "Неизвестно",
            "specs": recognized_text.strip()
        }

        return JSONResponse(content={"recognized": material_data})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при распознавании изображения: {str(e)}")
