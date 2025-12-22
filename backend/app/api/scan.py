# scan.py

# backend/app/api/scan.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

router = APIRouter(
    prefix="/scan",
    tags=["Warehouse Scan"],
)

# ===== ВХОД =====
class ScanRequest(BaseModel):
    image_url: HttpUrl


# ===== ВЫХОД =====
class ScanResponse(BaseModel):
    suggested_name: str | None = None
    suggested_brand: str | None = None
    suggested_model: str | None = None
    raw_text: str | None = None


@router.post("/material", response_model=ScanResponse)
async def scan_material(data: ScanRequest):
    """
    🔒 MOCK-распознавание.
    
    ❗️ВАЖНО:
    - Ничего не пишет в БД
    - Никакого OCR
    - Никаких новых полей
    - Только подсказки для UI
    
    Этот endpoint нужен, чтобы:
    - фронт был готов
    - Apple видел функциональность
    - OCR можно было подключить позже без изменения API
    """

    if not data.image_url:
        raise HTTPException(status_code=400, detail="image_url is required")

    # 🔹 Заглушка (стабильная, предсказуемая)
    return ScanResponse(
        suggested_name="Compressor",
        suggested_brand="Danfoss",
        suggested_model=None,
        raw_text="DANFOSS COMPRESSOR (mock)",
    )
