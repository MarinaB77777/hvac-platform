from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db import Base, engine
from app.api import (
    login,
    user_api,
    client_api,
    manager_api,
    warehouse_api,
    hvac_api,
    material_requests,
    materials,
)

from app.models.material import Material

app = FastAPI()

# CORS настройки (открыт для всех источников)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение всех роутеров
app.include_router(login.router)
app.include_router(user_api.router)
app.include_router(client_api.router)
app.include_router(manager_api.router)
app.include_router(warehouse_api.router)
app.include_router(hvac_api.router)
app.include_router(material_requests.router)
app.include_router(materials.router)

# Создание таблиц при первом запуске
Base.metadata.create_all(bind=engine)

# Ручное добавление колонок в таблицу materials (если не было Alembic)
@app.on_event("startup")
def add_missing_columns():
    with engine.connect() as connection:
        connection.execute(text("""
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS brand TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS material_type TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS specs TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_usd INTEGER;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_mxn INTEGER;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS stock INTEGER;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_date TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_to_hvac TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS qty_issued INTEGER;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS status TEXT;
        """))

# Debug endpoint для добавления тестового материала
@app.post("/debug/add-material")
def add_debug_material():
    from app.db import get_db
    db = next(get_db())

    material = Material(
        name="Компрессор X200",
        brand="Daikin",
        material_type="compressor",
        specs="220V, 3.5kW",
        price_usd=120,
        price_mxn=2100,
        stock=10,
        photo_url="https://example.com/photo.jpg",
        arrival_date="2024-06-01",
        issued_date=None,
        issued_to_hvac=None,
        qty_issued=0,
        status="на складе"
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return {"message": "Добавлен тестовый материал", "material_id": material.id}
