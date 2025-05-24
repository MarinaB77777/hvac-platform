from app.db import Base, engine
from app.models import user, order, warehouse, hvac_materials  # Добавь сюда все модули с моделями

print("Создание таблиц...")
Base.metadata.create_all(bind=engine)
print("Готово.")
