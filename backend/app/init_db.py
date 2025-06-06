from app.db import Base, engine
from app.models import user, order, warehouse, material_request, material  # ✅ добавлен material

print("Создание таблиц...")
Base.metadata.create_all(bind=engine)
print("Готово.")
