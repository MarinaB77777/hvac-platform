from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class MaterialUsage(Base):
    tablename = "material_usage"

    id = Column(Integer, primary_key=True, index=True)
    hvac_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    quantity_used = Column(Integer, nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)

    # 🔁 Опциональные связи
    hvac = relationship("User")
    material = relationship("Material")
