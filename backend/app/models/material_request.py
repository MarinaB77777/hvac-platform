from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class MaterialRequest(Base):
    tablename = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    hvac_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    qty = Column(Integer, nullable=False)
    status = Column(String, default="pending")
