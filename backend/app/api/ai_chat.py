# backend/app/api/ai_chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.db import get_db
from app.models.order import Order
from app.models.material_usage import MaterialUsage
from sqlalchemy.orm import Session

router = APIRouter(prefix="/ai-chat", tags=["ai-chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


# --- Simple timeframe parser (no external libs) ---
def parse_timeframe(text: str):
    now = datetime.utcnow()
    text = text.lower()

    if "today" in text:
        start = datetime(now.year, now.month, now.day)
        return start, now
    if "yesterday" in text:
        start = datetime(now.year, now.month, now.day) - timedelta(days=1)
        end = start + timedelta(days=1)
        return start, end
    if "week" in text:
        start = now - timedelta(days=7)
        return start, now
    if "month" in text:
        start = now - timedelta(days=30)
        return start, now

    return None, None


@router.post("/", response_model=ChatResponse)
def ai_chat(req: ChatRequest, db: Session = next(get_db())):
    msg = req.message.lower()

    # --- Orders related ---
    if "orders" in msg:
        start, end = parse_timeframe(msg)
        query = db.query(Order)
        if start and end:
            query = query.filter(Order.created_at >= start, Order.created_at <= end)

        count = query.count()
        return {"answer": f"There were {count} orders in the selected period."}

    # --- Materials related ---
    if "material" in msg or "warehouse" in msg:
        total = db.query(MaterialUsage).count()
        return {"answer": f"Total {total} material usage records in the system."}

    # --- Fallback ---
    return {"answer": "Sorry, I cannot answer this question yet. Please try asking about orders or warehouse."}
