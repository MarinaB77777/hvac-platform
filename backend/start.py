import uvicorn
from app.init_db import *  # Импортируем init_db.py, чтобы create_all выполнился

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=False)
