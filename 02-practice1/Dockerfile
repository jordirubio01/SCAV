# 1. Imatge base
FROM python:3.9-slim

# 2. (NOU) Instal·lem FFMPEG dins del contenidor
# Això compleix l'Exercici 2 del PDF
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

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