from fastapi import FastAPI
from app.api import material_requests

app = FastAPI()  # ← СНАЧАЛА создаем app

# Затем подключаем роутеры
app.include_router(material_requests.router)

# Корневая точка
@app.get("/")
def root():
    return {"message": "HVAC Platform API is up and running"}

# Другие роутеры и middleware
from fastapi.middleware.cors import CORSMiddleware
from app.api import login

app.include_router(login.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import warehouse_api
app.include_router(warehouse_api.router)
