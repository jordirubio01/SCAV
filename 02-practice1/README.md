# Pràctica 1: API & Dockerization

Aquest projecte implementa una API REST amb **FastAPI** encapsulada dins d'un contenidor **Docker** que inclou **FFMPEG**. Permet processar imatges i vídeos utilitzant lògica de la Sessió 1.

## 🛠️ Tecnologies
* Python 3.9
* FastAPI
* Docker & Docker Compose
* FFMPEG

## 🚀 Instal·lació i Execució

1. Cloneu el repositori:
   
   `git clone <https://github.com/jordirubio01/SCAV>`

2. Situeu-vos al directori:

   `cd 02-practice1`

3. Construïr les imatges:

   `docker-compose build`

4. Aixequeu els contenidors:

   `docker-compose up`

5. Accediu a la documentació interactiva de FastAPI:

   `http://localhost:8000/docs`

6. Si voleu processar algun arxiu nou, afegiu-lo a la carpeta:

   `./videos`

## 📖 Tasques

1. Task 1
   
   Hem creat una subcarpeta anomenada `02-Practice1`, on tenim els arxius `main.py`, `requirements.txt`, `Dockerfile` i `docker-compose.yml`.

   L'arxiu `main.py`conté l'aplicació FastAPI, l'arxiu `requirements.txt` inclou les llibreries necessàries per a aquesta API (`fastapi`, `uvicorn`, `pydantic`).

   L'arxiu `Dockerfile`descriu com es construeix la imatge Docker amb Python, com s'instal·len les dependències i com s'arranca l'API amb Uvicorn. El `docker-compose.yml`defineix el servei `video-api`, que utilitza aquesta imatge, exposa el port 8000 i crea la carpeta `videos`. Aquí és un fiquem l'API dins d'un contenidor Docker executable.

2. Task 2

   Dins de l'arxiu `Dockerfile`, instal·lem FFMPEG dins del contenidor. Abans utilitzàvem un mateix Docker, però ara tenim l'API i FFMPEG per separat.

3. Task 3

   A `main.py`, hem inclòs totes les funcions que teníem a l'anterior seminari, a l'script [`first_seminar`](https://github.com/jordirubio01/SCAV/blob/main/01-S1/first_seminar.py). Tenim: conversió RGB a YUV, compressió Run Length Encoding (RLE), processament d'imatges amb FFmpeg.

4. Task 4

   Hem creat dos endpoints:

   - Endpoint /converter/rgb-to-yuv: Processa l'acció de la classe ColorTranslator (RGB a YUV), adaptada amb endpoint FastApi amb un model Pydantic (RGBInput).
   - Endpoint /algorithm/rle: Processa l'acció de l'algoritme de compressió RLE, s'exposa com endpoint que rep un vector i retorna la versió comprimida juntament amb el ratio.