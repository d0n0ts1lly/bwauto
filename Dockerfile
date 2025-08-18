# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Скопируем зависимости и установим
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Указываем порт
EXPOSE 5000

# Запускаем через Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
