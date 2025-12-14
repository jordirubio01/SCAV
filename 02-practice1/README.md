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
   
   Hem creat una subcarpeta anomenada `02-Practice1`, on tenim l'arxiu `docker-compose.yml`. A més tenim dues subcarpetes `/api` i `/ffmpeg`, amb `main.py`, `requirements.txt`, `Dockerfile` cadascuna, i una carpeta compartida `/videos`.

   L'arxiu `main.py`conté l'aplicació FastAPI o el servei FFMPEG, l'arxiu `requirements.txt` inclou les llibreries necessàries.

   L'arxiu `Dockerfile`descriu com es construeix la imatge Docker amb Python, com s'instal·len les dependències i com s'arranca l'API amb Uvicorn. El `docker-compose.yml`defineix el servei `video-api`, que utilitza aquesta imatge, exposa el port 8000 (en el cas de l'API) i crea la carpeta `videos`. Aquí és on fiquem l'API dins d'un contenidor Docker executable.

2. Task 2

   Dins de l'arxiu `Dockerfile` de la carpeta `/ffmpeg`, instal·lem FFMPEG dins del contenidor. Abans utilitzàvem un mateix Docker, però ara tenim l'API i FFMPEG per separat.

3. Task 3

   A `main.py`, hem inclòs totes les funcions que teníem a l'anterior seminari, a l'script [`first_seminar`](https://github.com/jordirubio01/SCAV/blob/main/01-S1/first_seminar.py). Tenim: conversió RGB a YUV, compressió Run Length Encoding (RLE), càlcul de DCT i DWT, serpentine, i processament d'imatges amb FFmpeg. A més, també tenim `tests.py`, que ens permet comprovar que tot funcioni correctament si l'executem.

4. Task 4

   Hem creat diversos endpoints:

   - Endpoint /converter/rgb-to-yuv: Processa l'acció de la classe ColorTranslator (RGB a YUV), adaptada amb endpoint FastApi amb un model Pydantic (RGBInput).
   - Endpoint /algorithm/rle: Processa l'acció de l'algoritme de compressió RLE, s'exposa com endpoint que rep un vector i retorna la versió comprimida juntament amb el ratio.
   - Endpoint /algorithm/serpentine: Implementa l'escaneig en zig-zag (serpentina) d'una matriu NxM, retornant el recorregut lineal.
   - Endpoint /algorithm/dct: Aplica la transformada DCT (Discrete Cosine Transform) a un bloc de píxels (idealment 8x8) i retorna els coeficients.
   - Endpoint /algorithm/dwt: Aplica la transformada DWT (Discrete Wavelet Transform, Haar) a una matriu i retorna els coeficients.
   - Endpoint /image/resize/{filename}: Redimensiona una imatge o vídeo a les dimensions especificades (width, height). Aquest endpoint delega l'acció al servei FFMPEG.
   - Endpoint /image/bw-compression/{filename}: Converteix un fitxer a blanc i negre i aplica una compressió forta (qscale=31). També delega l'acció al servei FFMPEG.

5. Task 5 

Hem implementat la comunicació entre contenidors per complir amb el requisit d'interacció. Quan l'usuari fa una petició a l'endpoint de *resize* (Port 8000), l'API utilitza la llibreria `requests` per enviar una ordre interna al contenidor `ffmpeg` (Port 9000). Ambdós comparteixen el volum `/videos`, permetent que un servei llegeixi el fitxer, el processi, i l'altre en verifiqui el resultat.

---
**Autors:** Jordi Rubio & Lluc Sayols

**Assignatura:** Sistemes de Codificació d'Àudio i Video
