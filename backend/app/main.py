from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.services import auth  # ✅ исправлено
from app.api import (
    client_api,
    manager_api,
    warehouse_api,
    hvac_api,
    material_requests,
)
from app.db import engine, get_db
from app.models.material import Material
from app.models.material_request import MaterialRequest

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Подключение роутеров
app.include_router(auth.router)
app.include_router(client_api.router)
app.include_router(manager_api.router)
app.include_router(warehouse_api.router)
app.include_router(hvac_api.router)
app.include_router(material_requests.router)  # ✅ обязательно

# 📦 Создание таблиц
Base.metadata.create_all(bind=engine)

# 🛠️ Миграции (добавление недостающих столбцов)
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS model TEXT"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS material_type TEXT"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS specs TEXT"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_usd INTEGER"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_mxn INTEGER"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS stock INTEGER"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url TEXT"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date TEXT"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_date TEXT"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS issued_to_hvac INTEGER"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS qty_issued INTEGER"))
    conn.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS status TEXT"))

# 🧪 Debug endpoint — вручную создать материал
@app.post("/debug/add-material")
def debug_add_material(db=next(get_db())):
    material = Material(
        name="Фреон R410",
        brand="DuPont",
        model="R410",
        material_type="фреон",
        specs="R410 11.3kg",
        price_usd=120,
        price_mxn=2100,
        stock=5,
        photo_url="https://example.com/freon.jpg",
        arrival_date="2025-06-19",
        status="available"
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material
