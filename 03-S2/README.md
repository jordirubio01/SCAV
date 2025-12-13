# Seminari 2: MPEG4 and more endpoints

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
   
   Hem partit de la feina feta a l'anterior pràctica, i ens hi hem descarregat vídeo Big Buck Bunny. Per fer-ho, ens hem descarregat el vídeo d'aquest [enllaç](https://download.blender.org/demo/movies/BBB/), el qual havíem trobat en aquest altre [enllaç](https://peach.blender.org/download/). Inicialment l'havíem descarregat en 4K, 60fps i format mp4, i ocupava 642 MB. En vista que el nostre ordinador trigava molt a processar la informació, hem utilitzat el vídeo en 1080p, 30fps i format mp4, el qual ocupa 263 MB. Aquest vídeo no l'hem inclòs al repositori, de manera que us l'haureu de descarregar i afegir-lo a la carpeta `/videos`.

   Quan modifiquem la resolució del vídeo de 1080p i 30fps, el procés triga aproximadament 2 min 30 s. Per reduir el temps de les proves, hem tallat el vídeo de 10 min 34 s a 1 min, la qual cosa permet fer proves en menys de 10 s. Dit això, el codi segueix sent el mateix. D'altra banda, quan redimensionem un vídeo, l'àudio el mantenim igual. Al principi ens n'havíem descuidat, i no se sentia res, però la solució ha estat una línia senzilla que copia l'àudio original.

---
**Autors:** Jordi Rubio & Lluc Sayols

**Assignatura:** Sistemes de Codificació d'Àudio i Video