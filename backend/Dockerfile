# 🐍 Базовый образ с Python
FROM python:3.11-slim

# 📍 Установка зависимостей системы, включая Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🏗 Установка рабочей директории
WORKDIR /app

# 🧾 Копирование зависимостей и установка Python-пакетов
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 📦 Копирование остального кода
COPY . .

# 🚀 Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
