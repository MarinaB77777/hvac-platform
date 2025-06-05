from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Создаем приложение сначала!
app = FastAPI()

# Импортируем все роутеры
from app.api import (
    login,
    material_requests,
    warehouse_api,
    orders,
    user_api,  # ← регистрация
)

# Подключаем роутеры
app.include_router(login.router)
app.include_router(material_requests.router)
app.include_router(warehouse_api.router)
app.include_router(orders.router)
app.include_router(user_api.router)

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "HVAC Platform API is up and running"}

# CORS для мобильного клиента
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
from app.init_db import *
