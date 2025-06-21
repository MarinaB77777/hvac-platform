from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.services.auth import get_current_user # ✅ исправлено
from app.api import (
    login,
    user_api,
    material_requests,
    warehouse_api,
    orders,
    manager_api,
    client_api,
    hvac_api,
    materials, 
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
app.include_router(login.router)
app.include_router(user_api.router)
app.include_router(client_api.router)
app.include_router(manager_api.router)
app.include_router(warehouse_api.router)
app.include_router(hvac_api.router)
app.include_router(material_requests.router)

# 📦 Создание таблиц
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS materials"))
Base.metadata.create_all(bind=engine)

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
