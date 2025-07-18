from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.api import hvac_materials
from app.db import Base
from app.api.warehouse_recognition import warehouse_recognition
from app.api import (
    login,
    user_api,
    client_api,
    manager_api,
    warehouse_api,
    hvac_api,
    material_requests,
    materials,
    orders,
)
from app.models.material import Material
from app.models.material_request import MaterialRequest
from app.models import material_usage
from app.models.material_usage import MaterialUsage
from app.api import material_usage

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
app.include_router(materials.router)
app.include_router(hvac_materials.router)
app.include_router(orders.router)
app.include_router(material_usage.router)
app.include_router(warehouse_recognition.router)

# 🛠 Подключение к БД
from app.db import engine

# ✅ Создание всех таблиц, включая users
Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS address VARCHAR;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS material_id INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests ALTER COLUMN order_id DROP NOT NULL;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests DROP COLUMN IF EXISTS name;
    """))
    conn.commit()
    
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE material_requests DROP COLUMN IF EXISTS qty;
    """))
    conn.commit()

# ✅ Полная миграция таблицы materials (все необходимые поля)
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
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS qty_received INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS qty_issued INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_to_hvac INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url TEXT;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date DATE;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_date DATE;
    """))
    conn.execute(text("""
        ALTER TABLE materials ADD COLUMN IF NOT EXISTS status VARCHAR;
    """))

# 📦 Полная миграция таблицы material_requests (все необходимые поля)
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS material_id INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS order_id INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS hvac_id INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS quantity INTEGER;
    """))
    conn.execute(text("""
        ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending';
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
