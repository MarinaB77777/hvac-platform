# backend/Dockerfile

FROM python:3.11-slim

# Обновление системы и установка зависимостей для easyocr и PIL
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей и установка Python-пакетов
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копирование исходного кода
COPY . .

# Запуск приложения
CMD ["python", "start.py"]
