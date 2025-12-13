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

2. Task 2

   Hem afegit un endpoint que permet modificar el chroma subsampling amb l'opció `-pix_fmt` de FFmpeg (per exemple "yuv420p", "yuv422p", "yuv444p").

3. Task 3

   Per trobar almenys 5 dades rellevants del vídeo, hem utilitzat `ffprobe` per obtenir metadades en format JSON. Aquest endpoint retorna la duració del vídeo en segons, la mida en bytes, el bitrate global, el còdec del vídeo, la resolució (amplada i alçada), còdec d'àudio i sample rate d'àudio.

4. Task 4

   En aquesta part, tallem els primers 20 segons del vídeo, i empaquetem tres formats diferents d'àudio (AAC mono, MP3 estèreo amb baix bitrate, AC3 estèreo o amb més canals segons l'original) en un mateix video MP4. Per poder escoltar els canvis entre les tres pistes d'àudio, hem utilitzat el reproductor VLC, que és un reproductor multimedia lliure i de codi obert ([enllaç](https://images.videolan.org/vlc/index.es.html)).

5. Task 5

   Aquesta tasca ha estat semblant a la 4, ja que també hem utilitzat `ffprobe` per llegir els streams d'un contenidor MP4 i retornar-ne la quantitat de pistes (vídeo, àudio, subtítols).

6. Task 6

   Per aquesta tasca, hem utilitzat el filtre `codecview` de FFmpeg, que permet visualitzar macroblocks i motion vectors. La comanda `-flags2 +export_mvs` activa l'exportació de motion vectors, i `codecview=mv=pf+bf+bb` mostra els vectors de moviment dels diferents tipus de frames (forward, backward i bidirectional). A més, hi hem afegit una quadrícula per a veure clarament els macroblocks.

7. Task 7

   En aquesta última tasca, hem utilitzat el filtre `histogram` de FFmpeg, que genera un vídeo on es mostra l'histograma YUV de cada frame. Com a curiositat, al principi no podíem reproduir l'histograma amb el Reproductor Multimedia de Windows, però sí amb VLC. Per fer-ho més còmode, finalment hem decidit exportar l'histograma en format yuv420p amb `"-pix_fmt", "yuv420p"` (canviem el format de sortida, un cop ja hem analitzat l'histograma), de manera que sigui compatible amb el reproductor de Windows.

---
**Autors:** Jordi Rubio & Lluc Sayols

**Assignatura:** Sistemes de Codificació d'Àudio i Video