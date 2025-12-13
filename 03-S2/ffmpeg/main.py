from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Data Models
class ResizeInput(BaseModel):
    width: int
    height: int

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