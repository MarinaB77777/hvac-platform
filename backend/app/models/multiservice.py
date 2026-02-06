from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.db import Base

class MultiService(Base):
    __tablename__ = "multiservices"

    id = Column(Integer, primary_key=True, index=True)

    # уникальный код с префиксом multiservice-
    multiservice_code = Column(String, unique=True, index=True, nullable=False)

    # название услуги (то, что видит клиент)
    title = Column(String, index=True, nullable=False)

    # подробности / список возможностей (пока строкой, можно потом JSON)
    details = Column(String, nullable=True)

    # HVAC настройки (чтобы убрать фикс из кода)
    road_tariff = Column(Integer, nullable=True)        # цена дороги/вызова
    diagnostic_price = Column(Integer, nullable=True)   # цена диагностики

    # эти суммы “берём из существующей логики”, но можно хранить дефолт/0
    materials_default = Column(Integer, nullable=True)  # дефолт (не обязательно)
    base_price = Column(Integer, nullable=True)         # прайс для новых услуг (handyman/cleaning)

    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # использовалась ли услуга хотя бы раз (чтобы запрещать удаление)
    is_used = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
