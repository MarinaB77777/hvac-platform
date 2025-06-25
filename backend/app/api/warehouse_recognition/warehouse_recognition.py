# backend/app/api/warehouse_recognition/warehouse_recognition.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import numpy as np
import cv2

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse-ocr"]
)

@router.post("/recognize-image")
async def recognize_text_from_image(image: UploadFile = File(...)):
    try:
        # Чтение содержимого изображения
        contents = await image.read()

        # Декодирование изображения через OpenCV
        nparr = np.frombuffer(contents, np.uint8)
        cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if cv_img is None:
            raise HTTPException(status_code=400, detail="Не удалось декодировать изображение")

        # Предобработка: серое изображение + бинаризация
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Преобразование обратно в формат PIL
        img = Image.fromarray(thresh)

        # Распознавание текста через pytesseract
        text = pytesseract.image_to_string(img)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Текст не распознан")

        return JSONResponse(status_code=200, content={"text": text.strip()})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR ошибка: {str(e)}")
