from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class MaterialRequest(Base):
    __tablename__ = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    order_id = Column(Integer, nullable=True)
    hvac_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")

    material = relationship("Material", lazy="joined")
