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

# 6. Copiem la configuració d'Streamlit
RUN mkdir -p /root/.streamlit
COPY config.toml /root/.streamlit/config.toml

# 7. Exposem el port
EXPOSE 8501

# 8. Comanda d'inici
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]