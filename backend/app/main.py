from fastapi import FastAPI
from app.api import material_requests
app.include_router(material_requests.router)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HVAC Platform API is up and running"}


from fastapi.middleware.cors import CORSMiddleware
from app.api import login

app.include_router(login.router)

# CORS (если фронт отдельно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import order
app.include_router(order.router)

from app.api import materials
app.include_router(materials.router)

from app.api import hvac_materials
app.include_router(hvac_materials.router)

from app.api import analytics
app.include_router(analytics.router)

from app.api import hvac_users
app.include_router(hvac_users.router)

from app.api import warehouse_api
app.include_router(warehouse_api.router)
