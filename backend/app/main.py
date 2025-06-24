from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.api import (
    login,
    user_api,
    client_api,
    manager_api,
    warehouse_api,
    hvac_api,
    material_requests,
    orders,
)
from app.models.material import Material
from app.models.material_request import MaterialRequest

app = FastAPI()

# 🔓 CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Роутеры
app.include_router(login.router)
app.include_router(user_api.router)
app.include_router(client_api.router)
app.include_router(manager_api.router)
app.include_router(warehouse_api.router)
app.include_router(hvac_api.router)
app.include_router(material_requests.router)
app.include_router(orders.router)

# 🛠 Подключение к БД
from app.db import engine

# ✅ Ручная миграция таблицы materials (без material_type)
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS name VARCHAR;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS model VARCHAR;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS brand VARCHAR;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS specs VARCHAR;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_usd FLOAT;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_mxn FLOAT;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS stock INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url TEXT;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date DATE;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS status VARCHAR;
    """))
    conn.commit()

# ✅ Вставка тестового материала (без material_type)
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM materials"))
    count = result.scalar()
    if count == 0:
        conn.execute(text("""
            INSERT INTO materials (
                name, model, brand, specs,
                price_usd, price_mxn, stock,
                photo_url, arrival_date, status
            ) VALUES (
                'Деталь тестовая', 'X-200', 'LG', 'модель X-200',
                100.0, 1800.0, 10,
                'https://example.com/photo.jpg', '2024-06-20', 'available'
            )
        """))
        conn.commit()
