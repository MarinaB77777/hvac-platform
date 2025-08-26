from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime 
from app.db import Base

class MaterialRequest(Base):
    __tablename__ = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    order_id = Column(Integer, nullable=True)
    hvac_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    issued_date = Column(DateTime, default=datetime.utcnow)
    price_usd = Column(Float, nullable=True)
    price_mxn = Column(Float, nullable=True)

    material = relationship("Material", backref="requests")  # для joined view
