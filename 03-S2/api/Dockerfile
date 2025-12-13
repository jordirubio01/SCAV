# 1. Imatge base
FROM python:3.9-slim

# 2. (NOU) Instal·lem FFMPEG dins del contenidor
# No cal instal·lar ffmpeg dins d'aquest docker

# 3. Directori de treball
WORKDIR /app

# 4. Dependències Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiem el codi
COPY . .

# 6. Exposem el port
EXPOSE 8000

# 7. Comanda d'inici
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]