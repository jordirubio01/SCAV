from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import os
import numpy as np 

app = FastAPI()

# Data Models
class RGBInput(BaseModel):
    r: int
    g: int
    b: int

class RLEInput(BaseModel):
    data: List[int]

class ResizeInput(BaseModel):
    width: int
    height: int

# Auxiliar function
def run_length_encoding_logic(data):
    encoded = []
    i = 0
    while i < len(data):
        if data[i] != 0:
            encoded.append(data[i])
            i += 1
        else:
            count = 0
            while i < len(data) and data[i] == 0:
                count += 1
                i += 1
            encoded.append(0)
            encoded.append(count)
    return encoded

# --- ENDPOINTS DE L'API ---

@app.get("/")
def read_root():
    return {"message": "API Sessió 1 Integrada amb Docker i FFMPEG"}


# Color conversor

@app.post("/converter/rgb-to-yuv")
def convert_rgb_to_yuv(color: RGBInput):
    """
    Implementació de la teva classe ColorTranslator via API
    """
    Y =  0.257 * color.r + 0.504 * color.g + 0.098 * color.b + 16
    U = -0.148 * color.r - 0.291 * color.g + 0.439 * color.b + 128
    V =  0.439 * color.r - 0.368 * color.g - 0.071 * color.b + 128
    
    return {
        "input_rgb": {"r": color.r, "g": color.g, "b": color.b},
        "output_yuv": {"y": round(Y, 2), "u": round(U, 2), "v": round(V, 2)}
    }


# Run Length Encoding
@app.post("/algorithm/rle")
def perform_rle(payload: RLEInput):
    """
    Executa el teu algoritme de compressió RLE sobre una llista de números.
    """
    result = run_length_encoding_logic(payload.data)
    compression_ratio = 0
    if len(payload.data) > 0:
        compression_ratio = (1 - (len(result) / len(payload.data))) * 100
        
    return {
        "input_length": len(payload.data),
        "encoded_data": result,
        "encoded_length": len(result),
        "compression_ratio_percent": round(compression_ratio, 2)
    }

# Resize Image
@app.post("/image/resize/{filename}")
def resize_image(filename: str, settings: ResizeInput):
    """
    Fa servir FFMPEG dins del Docker per redimensionar una imatge/vídeo
    """
    # Rutes dins del Docker
    input_path = f"videos/{filename}"
    output_filename = f"resized_{settings.width}x{settings.height}_{filename}"
    output_path = f"videos/{output_filename}"

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"El fitxer {filename} no existeix a la carpeta 'videos'")

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
        raise HTTPException(status_code=500, detail=f"Error FFMPEG: {str(e)}")

# BW Hard Compression
@app.post("/image/bw-compression/{filename}")
def compress_bw(filename: str):
    """
    Converteix a blanc i negre i comprimeix al màxim (qscale 31)
    """
    input_path = f"videos/{filename}"
    output_filename = f"bw_compressed_{filename}"
    output_path = f"videos/{output_filename}"

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
        
        # Calculem la reducció de mida com feies tu
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