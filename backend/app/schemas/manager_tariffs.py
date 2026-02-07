from pydantic import BaseModel, Field

class ApplyRoadTariffPayload(BaseModel):
    tarif: int = Field(..., ge=0)

class ApplyLaborRatePayload(BaseModel):
    rate: int = Field(..., ge=0, le=100)
