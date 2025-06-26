# Базовый образ с Python и полноценной системой
FROM python:3.11-bullseye

# Установка системных библиотек, включая Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Указываем путь к tesseract на всякий случай
ENV TESSERACT_CMD=/usr/bin/tesseract

# Запуск приложения
CMD ["python", "start.py"]
