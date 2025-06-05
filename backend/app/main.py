from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    login,
    material_requests,
    warehouse_api,
    orders,  # ← ДОБАВЬ ЭТО
)

app = FastAPI()

# Подключаем роутеры
app.include_router(login.router)
app.include_router(material_requests.router)
app.include_router(warehouse_api.router)
app.include_router(orders.router)  # ← ОБЯЗАТЕЛЬНО

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "HVAC Platform API is up and running"}

# Разрешаем CORS (кросс-доменные запросы)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from app.init_db import *
