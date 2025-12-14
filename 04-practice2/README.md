# Practice 2: Transcoding

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

   `cd 04-practice2`

3. Construïr les imatges:

   `docker-compose build`

4. Aixequeu els contenidors:

   `docker-compose up`

5. Accediu a la documentació interactiva de FastAPI:

   `http://localhost:8000/docs`

6. Si voleu processar algun arxiu nou, afegiu-lo a la carpeta:

   `./videos`

7. Per fer servir la GUI, utilitzeu el web local:

   `http://localhost:8501`

## 📖 Tasques

1. Task 1
   
   En aquesta primera tasca, convertim un vídeo a quatre còdecs diferents: VP8 i VP9 (contenidor `.webm` amb `libvpx` i `libvpx-vp9`), H.265 (contenidor `.mp4` amb `libx265`), i AV1 (contenidor `.mkv` amb `libaom-av1`). Aquest endpoint genera les quatre sortides a la vegada. Cal dir que triga força en executar, especialment amb H264 i AV1 que precisament són còdecs més nous, que comprimeixen molt més i que, per tant, tenen una complexitat de càlcul major. A més, en aquestes proves estem utilitzant la CPU, mentre que habitualment per a aquestes codificacions s'utilitza la GPU o llibreries d'acceleració.

2. Task 2

   Aquí volem construir un encoding ladder, és a dir diverses versions d'un mateix vídeo amb diferents resolucions i bitrates. Hem definit una funció auxiliar per a codificar a un cert còdec, i l'hem utilitzat en un nou endpoint per a fer l'Encoding Ladder.

3. Task 3

   Fins ara, tenim un API que permet fer diversos processos amb imatges i vídeos. Per crear una interfície gràfica, hi ha moltes opcions. Dit això, com que hem anat justos de temps i a més ja hi hem treballat en altres ocasions, hem decidit utilitzar Streamlit.

   En primer lloc, hem creat un nou servei, com API i FFMPEG, anomenat GUI. Aquest també comparteix les dades de la carpeta `./videos:/data`. Aquest servei utilitza el port 8501, que és el predeterminat per a Streamlit.

4. Task 4

   Finalment hem utilitzat intel·ligència artificial (IA) per a optimitzar parts del codi. Per exemple, a la conversió en diferents còdecs, i en particular per al codec av1 .mkv, hem utilitzat paràmetres com `-preset`, `-threads`, `-tile-columns`, `-tile-rows` per accelerar una mica el procés, ja que només volem fer proves.

---
**Autors:** Jordi Rubio & Lluc Sayols

**Assignatura:** Sistemes de Codificació d'Àudio i Video