# Використовуємо базовий образ Python для asyncio та aiohttp
FROM python:3.11-slim

# Встановлюємо залежності для сервера
RUN pip install websockets aiohttp names

# Копіюємо файли сервера та веб-сайту в контейнер
COPY server.py /app/server.py
COPY index.html /app/index.html
COPY index.js /app/index.js
COPY index.css /app/index.css
COPY extra.py /app/extra.py

# Встановлюємо робочий каталог
WORKDIR /app

# Виконуємо команду для запуску сервера та веб-сервера при старті контейнера
CMD ["bash", "-c", "python server.py & python -m http.server 8000"]
