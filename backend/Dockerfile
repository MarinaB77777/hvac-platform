# backend/Dockerfile

FROM python:3.11-slim

# 📌 Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🗂 Рабочая директория
WORKDIR /app

# 📦 Копируем зависимости и устанавливаем Python-библиотеки
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 📁 Копируем всё приложение внутрь контейнера
COPY . .

# 🚀 Старт сервера
CMD ["python", "start.py"]
