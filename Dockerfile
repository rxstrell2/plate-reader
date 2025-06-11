FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 wget libsm6 libxext6 libxrender-dev libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем проект
WORKDIR /app
COPY . .

# Установка Python-зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Порт для Flask
ENV PORT=8080

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
