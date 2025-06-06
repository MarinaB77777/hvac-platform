from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    login,
    user_api,
    material_requests,
    warehouse_api,
    orders
)

from app.db import engine
from sqlalchemy import text

app = FastAPI()

# 🔗 Подключаем роутеры
app.include_router(login.router)
app.include_router(user_api.router)
app.include_router(material_requests.router)
app.include_router(warehouse_api.router)
app.include_router(orders.router)

# 🌍 CORS (разрешаем запросы с любых источников)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📍 Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "HVAC Platform API is up and running"}

# 🔧 Добавляем недостающие столбцы, если нужно
from sqlalchemy.exc import SQLAlchemyError

with engine.begin() as conn:  # begin = отдельная транзакция на каждую итерацию
    def safe_alter(sql):
        try:
            conn.execute(text(sql))
            print(f"✅ {sql}")
        except SQLAlchemyError as e:
            print(f"⚠️ Пропущено: {sql} — {e}")

    print("\n🔧 Проверка и добавление недостающих столбцов...")

    # Таблица users
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS location VARCHAR;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS qualification VARCHAR;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS rate INTEGER;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR;")

    # Таблица materials
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS brand VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS stock_count INTEGER;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS status VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date DATE;")

    # Таблица material_requests
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS order_id INTEGER;")
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS hvac_id INTEGER;")
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS quantity INTEGER;")
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS status VARCHAR;")

    # Таблица orders
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS location VARCHAR;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS description TEXT;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS diagnostic_url VARCHAR;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS client_agreed BOOLEAN DEFAULT false;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS repair_cost INTEGER;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")

    print("🔧 Готово.\n")
