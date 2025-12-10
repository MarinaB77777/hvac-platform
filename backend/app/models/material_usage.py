from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class MaterialUsage(Base):
    __tablename__ = "material_usage"

    id = Column(Integer, primary_key=True, index=True)
    hvac_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    quantity_used = Column(Integer, nullable=False)
    used_date = Column(DateTime, default=datetime.utcnow)
    

    # Копии данных из материала на момент использования
    name = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    specs = Column(String, nullable=True)
    price_usd = Column(Integer, nullable=True)
    price_mxn = Column(Integer, nullable=True)
    organization = Column(Text, nullable=True)

    hvac = relationship("User", backref="used_materials")
    material = relationship("Material", backref="usages")
    order = relationship("Order", backref="material_usages")
    


