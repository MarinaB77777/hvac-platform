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
        print("📦 Изображение получено, размер:", len(contents))

        image_obj = Image.open(BytesIO(contents))
        print("🖼 Изображение открыто")

        recognized_text = pytesseract.image_to_string(image_obj)
        print("📄 Распознанный текст:", recognized_text)

        material_data = {
            "name": "Неизвестно",
            "brand": "Неизвестно",
            "model": "Неизвестно",
            "recognized_text": recognized_text,
        }

        return JSONResponse(content={"status": "ok", "data": material_data})

    except Exception as e:
        print("❌ Ошибка при распознавании изображения:", str(e))
        raise HTTPException(status_code=500, detail=f"Ошибка при распознавании изображения: {str(e)}")
