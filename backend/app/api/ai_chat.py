# backend/app/api/ai_chat.py
# backend/app/api/ai_chat.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.db import get_db
from app.models.order import Order
from app.models.material_usage import MaterialUsage
from app.models.user import User
from app.services.auth import get_current_user
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
def ai_chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    msg = req.message.lower()
    manager_org = current_user.organization

    # --- Orders related ---
    if "orders" in msg:
        start, end = parse_timeframe(msg)
        query = db.query(Order).join(User, Order.hvac_id == User.id).filter(User.organization == manager_org)
        if start and end:
            query = query.filter(Order.created_at >= start, Order.created_at <= end)

        count = query.count()
        return {"answer": f"There were {count} orders in your organization during the selected period."}

    # --- Materials related ---
    if "material" in msg or "warehouse" in msg:
        total = (
            db.query(MaterialUsage)
            .join(User, MaterialUsage.hvac_id == User.id)
            .filter(User.organization == manager_org)
            .count()
        )
        return {"answer": f"Total {total} material usage records in your organization."}

    # --- Fallback ---
    return {"answer": "Sorry, I cannot answer this question yet. Please try asking about orders or warehouse."}
