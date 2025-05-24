from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base

class MaterialRequest(Base):
    __tablename__ = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    hvac_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String)
    qty = Column(Integer, nullable=False)
    status = Column(String, default="pending")
