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

# CORS настройки
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

# Основная попытка создания таблиц (если модели описаны корректно)
Base.metadata.create_all(bind=engine)

# ⬇️ Ручное создание таблицы materials (если совсем нет)
@app.post("/debug/create-materials-table")
def create_materials_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS materials (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                model TEXT,
                brand TEXT,
                material_type TEXT,
                specs TEXT,
                price_usd FLOAT,
                price_mxn FLOAT,
                stock INTEGER DEFAULT 0 NOT NULL,
                photo_url TEXT,
                arrival_date DATE,
                issued_date DATE,
                issued_to_hvac INTEGER,
                qty_issued INTEGER,
                status TEXT DEFAULT 'available'
            );
        """))
    return {"status": "created"}

# ⬇️ Добавление недостающих колонок вручную (если таблица есть, но неполная)
@app.post("/debug/fix-materials-columns")
def fix_materials_columns():
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS name TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS model TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS brand TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS material_type TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS specs TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_usd FLOAT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_mxn FLOAT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS stock INTEGER DEFAULT 0;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url TEXT;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date DATE;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_date DATE;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_to_hvac INTEGER;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS qty_issued INTEGER;
            ALTER TABLE materials ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'available';
        """))
    return {"status": "columns ensured"}

# ⬇️ Debug: список колонок таблицы materials
@app.get("/debug/columns/materials")
def get_material_columns():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'materials'
        """))
        return [{"column": row[0], "type": row[1]} for row in result]

from sqlalchemy import text

@app.on_event("startup")
def insert_initial_material():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM materials"))
        count = result.scalar()  # ← 🛠 ВЕРНУТЬ ЭТУ СТРОКУ

        if count == 0:
            conn.execute(text("""
                INSERT INTO materials (
                    name, material_type, brand, specs,
                    price_usd, price_mxn, stock,
                    photo_url, arrival_date, status
                ) VALUES (
                    'Деталь тестовая', 'Компрессор', 'LG', 'модель X-200',
                    100.0, 1800.0, 10,
                    'https://example.com/photo.jpg', '2024-06-20', 'available'
                )
            """))
            conn.commit()

# ⬇️ Debug: добавление тестового материала
@app.post("/debug/add-material")
def add_debug_material():
    from app.db import get_db
    db = next(get_db())

    material = Material(
        name="Компрессор",
        model="X200",
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
