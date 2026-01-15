FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY app/ ./app/

# Создание директории для базы данных
RUN mkdir -p /data

# Переменная окружения для базы данных
ENV DB_PATH=/data/leads.db

# Запуск бота
CMD ["python", "-m", "app.bot"]
