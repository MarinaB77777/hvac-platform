from fastapi import APIRouter, Query

router = APIRouter()

# Простой mock-справочник материалов
materials_db = [
    {"name": "Фреон", "brand": "R410", "unit_price": 15},
    {"name": "Компрессор", "brand": "Hitachi", "unit_price": 120},
    {"name": "Фильтр", "brand": "Panasonic", "unit_price": 40},
    {"name": "Термостат", "brand": "Danfoss", "unit_price": 60}
]

@router.get("/materials/")
def list_materials(q: str = Query(default=None)):
    if q:
        q_lower = q.lower()
        return [
            m for m in materials_db
            if q_lower in m["name"].lower() or q_lower in m["brand"].lower()
        ]
    return materials_db
