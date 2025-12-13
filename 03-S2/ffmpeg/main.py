from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Data Models
class ResizeInput(BaseModel):
    width: int
    height: int

class ChromaInput(BaseModel):
    subsampling: str  # p.e. "yuv420p", "yuv422p", "yuv444p"

# --- ENDPOINTS DE L'API ---

@app.get("/")
def read_root():
    return {"message": "Servei FFMPEG preparat"}


# Resize Image
@app.post("/image/resize/{filename}")
def resize_image(filename: str, settings: ResizeInput):
    """
    Redimensionar una imatge/vídeo
    """
    # Rutes dins del Docker
    input_path = f"/data/{filename}"
    output_filename = f"resized_{settings.width}x{settings.height}_{filename}"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # ffmpeg -i input -vf scale=w:h output
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"scale={settings.width}:{settings.height}",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        return {"status": "success", "output_file": output_filename}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")


# BW Hard Compression (utilitza l'altre Docker amb FFMPEG)
@app.post("/image/bw-compression/{filename}")
def compress_bw(filename: str):
    """
    Convertir a blanc i negre i comprimir al màxim (qscale 31)
    """
    input_path = f"/data/{filename}"
    output_filename = f"bw_compressed_{filename}"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Fitxer no trobat")

    # Comanda: ffmpeg -i input -vf hue=s=0 -q:v 31 output
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", "hue=s=0",
        "-q:v", "31",
        output_path
    ]

    try:
        subprocess.run(command, check=True)

        # Calculem la reducció de mida
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        ratio = (1 - (new_size / original_size)) * 100

        return {
            "status": "compressed",
            "original_size": original_size,
            "compressed_size": new_size,
            "compression_ratio": f"{round(ratio, 2)}%",
            "output_file": output_filename
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error FFMPEG: {str(e)}")
    

# Canviar Resolució Vídeo (utilitza l'altre Docker amb FFMPEG)
@app.post("/video/change-resolution/{filename}")
def change_resolution(filename: str, settings: ResizeInput):
    """
    Canviar la resolució d'un vídeo utilitzant FFMPEG
    """
    input_path = f"/data/{filename}"
    output_filename = f"changed_res_{settings.width}x{settings.height}_{filename}"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # ffmpeg -i input -vf scale=w:h output
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"scale={settings.width}:{settings.height}",
        "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        # Calculem mides per mostrar la reducció
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        ratio = (1 - (new_size / original_size)) * 100

        return {
            "status": "resolution_changed",
            "original_size": original_size,
            "new_size": new_size,
            "compression_ratio": f"{round(ratio, 2)}%",
            "output_file": output_filename
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")
    
# Canviar Chroma Subsampling
@app.post("/video/chroma-subsampling/{filename}")
def change_chroma_subsampling(filename: str, settings: ChromaInput):
    """
    Modificar el chroma subsampling d'un vídeo (ej: yuv420p, yuv422p, yuv444p)
    """
    input_path = f"/data/{filename}"
    output_filename = f"chroma_{settings.subsampling}_{filename}"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # ffmpeg -i input -pix_fmt yuv420p output
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-pix_fmt", settings.subsampling,
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        ratio = (1 - (new_size / original_size)) * 100

        return {
            "status": "chroma_changed",
            "original_size": original_size,
            "new_size": new_size,
            "compression_ratio": f"{round(ratio, 2)}%",
            "output_file": output_filename,
            "pix_fmt": settings.subsampling
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")

# Informació del Vídeo
@app.get("/video/info/{filename}")
def get_video_info(filename: str):
    """
    Llegeix informació del vídeo utilitzant ffprobe i retorna dades rellevants.
    """
    input_path = f"/data/{filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # ffprobe -v error -show_entries format=duration,size,bit_rate -show_streams -of json input
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration,size,bit_rate",
        "-show_streams",
        "-of", "json",
        input_path
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        import json
        info = json.loads(result.stdout)

        # Seleccionem algunes dades rellevants
        format_info = info.get("format", {})
        streams = info.get("streams", [])

        video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

        return {
            "filename": filename,
            "duration_seconds": format_info.get("duration"),
            "size_bytes": format_info.get("size"),
            "bit_rate": format_info.get("bit_rate"),
            "video_codec": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "audio_codec": audio_stream.get("codec_name"),
            "sample_rate": audio_stream.get("sample_rate")
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error ffprobe: {str(e)}")
    
# Big Buck Bunny Container
@app.post("/video/create-bbb-container/{filename}")
def create_bbb_container(filename: str):
    """
    Crea un contenidor MP4 amb:
    - Vídeo BBB retallat a 20s
    - Àudio AAC mono
    - Àudio MP3 stereo amb bitrate baix
    - Àudio AC3
    """
    input_path = f"/data/{filename}"
    name, ext = os.path.splitext(filename)
    output_filename = f"bbb_container_{name}.mp4"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # Comanda ffmpeg:
    # -ss 0 -t 20 retalla els primers 20s
    # -map 0:v:0 agafa el vídeo original
    # -map 0:a:0 agafa l'àudio original i crea múltiples còdecs
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ss", "0", "-t", "20",
        # Vídeo original
        "-map", "0:v:0", "-c:v", "copy",
        # AAC mono
        "-map", "0:a:0", "-c:a:0", "aac", "-ac:a:0", "1",
        # MP3 stereo amb bitrate baix
        "-map", "0:a:0", "-c:a:1", "mp3", "-b:a:1", "64k", "-ac:a:1", "2",
        # AC3
        "-map", "0:a:0", "-c:a:2", "ac3",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        return {
            "status": "bbb_container_created",
            "output_file": output_filename,
            "duration": "20s",
            "audio_tracks": ["aac mono", "mp3 stereo 64k", "ac3"]
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")
    
# Nombre de Tracks del Contenidor
@app.get("/video/tracks/{filename}")
def count_tracks(filename: str):
    """
    Llegeix un contenidor MP4 i retorna quantes pistes (streams) té.
    """
    input_path = f"/data/{filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # ffprobe -v error -show_streams -of json input
    command = [
        "ffprobe",
        "-v", "error",
        "-show_streams",
        "-of", "json",
        input_path
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        import json
        info = json.loads(result.stdout)

        streams = info.get("streams", [])
        num_tracks = len(streams)

        # Opcional: detalle por tipo de pista
        track_types = [s.get("codec_type") for s in streams]

        return {
            "filename": filename,
            "num_tracks": num_tracks,
            "track_types": track_types
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error ffprobe: {str(e)}")
    
# Mostrar Macroblocks i Motion Vectors
@app.post("/video/show-motion/{filename}")
def show_motion_vectors(filename: str):
    """
    Genera un vídeo amb macroblocks i vectors de moviment visibles.
    """
    input_path = f"/data/{filename}"
    output_filename = f"motion_vectors_{filename}"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # Comanda FFmpeg amb codecview
    command = [
        "ffmpeg", "-y",
        "-flags2", "+export_mvs",
        "-i", input_path,
        "-vf", "drawgrid=width=16:height=16:thickness=1:color=white,codecview=mv=pf+bf+bb",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        return {
            "status": "motion_vectors_generated",
            "output_file": output_filename,
            "description": "Vídeo amb macroblocks i vectors de moviment visibles"
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")
    
# Mostrar Histograma YUV
@app.post("/video/yuv-histogram/{filename}")
def show_yuv_histogram(filename: str):
    """
    Genera un vídeo amb l'histograma YUV visible
    """
    input_path = f"/data/{filename}"
    output_filename = f"yuv_histogram_{filename}"
    output_path = f"/data/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'data'")

    # Comanda FFmpeg amb filtre histogram
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", "histogram",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        return {
            "status": "yuv_histogram_generated",
            "output_file": output_filename,
            "description": "Vídeo amb histograma YUV visible"
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")