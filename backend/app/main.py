from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db import engine, Base

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

# Импорт всех моделей
from app.models import user, order, warehouse, material_request, material

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HVAC Platform API is up and running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(user_api.router)
app.include_router(material_requests.router)
app.include_router(warehouse_api.router)
app.include_router(orders.router)
app.include_router(manager_api.router)
app.include_router(client_api.router)
app.include_router(hvac_api.router)
app.include_router(materials.router)

print("⏳ Пробуем создать все таблицы...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Все таблицы созданы.")
except Exception as e:
    print("⚠️ Не удалось создать таблицы:", e)

with engine.connect() as conn:
    def safe_alter(sql):
        try:
            conn.execute(text(sql))
            print(f"✅ Выполнено: {sql}")
        except Exception as e:
            print(f"⚠️ Пропущено: {sql} — {e}")

    print("\n🔧 Добавление нужных столбцов:")

    # 🔹 Таблица users
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS location VARCHAR;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS qualification VARCHAR;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS rate INTEGER;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR;")
    safe_alter("ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR;")

    # 🔹 Таблица materials
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS stock INTEGER;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS category VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS brand VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS specs VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_usd INTEGER;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS price_mxn INTEGER;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS photo_url VARCHAR;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS arrival_date DATE;")
    safe_alter("ALTER TABLE materials ADD COLUMN IF NOT EXISTS status VARCHAR;")

    # 🔹 Таблица material_requests
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS order_id INTEGER;")
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS hvac_id INTEGER;")
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS quantity INTEGER;")
    safe_alter("ALTER TABLE material_requests ADD COLUMN IF NOT EXISTS status VARCHAR;")

    # 🔹 Таблица orders
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS location VARCHAR;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS description TEXT;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS diagnostic_url VARCHAR;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS client_agreed BOOLEAN DEFAULT false;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS repair_cost INTEGER;")
    safe_alter("ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")

    print("🔧 Добавление завершено.\n")

# 🛠️ Жёсткая вставка на случай, если category не добавляется
def ensure_category_column_exists():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'materials' AND column_name = 'category';
        """))
        if not result.fetchone():
            conn.execute(text('ALTER TABLE materials ADD COLUMN category VARCHAR;'))
            print("✅ [Hard] Колонка 'category' добавлена вручную")
        else:
            print("ℹ️ [Hard] Колонка 'category' уже существует")

ensure_category_column_exists()
