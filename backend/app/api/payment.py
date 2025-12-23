from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)

class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    currency: str = "USD"

class PaymentResponse(BaseModel):
    status: str
    transaction_id: str | None = None

@router.post("/pay", response_model=PaymentResponse)
async def mock_payment(data: PaymentRequest):
    return PaymentResponse(
        status="success",
        transaction_id=f"mock_tx_{data.order_id}",
    )
