FROM python:3.10-slim

# 🧩 Устанавливаем tesseract и зависимости
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 🔧 Устанавливаем рабочую директорию
WORKDIR /app

# 📦 Копируем зависимости
COPY requirements.txt .

# 🐍 Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 📁 Копируем весь проект
COPY . .

# 🚀 Запуск через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
