from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import os
import requests
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
    return {"message": "API Sessió 1 Integrada amb Docker i FFMPEG (separats)"}


# Color conversor

@app.post("/converter/rgb-to-yuv")
def convert_rgb_to_yuv(color: RGBInput):
    """
    Implementació de la classe ColorTranslator via API
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

# Resize Image (utilitza l'altre Docker amb FFMPEG)
@app.post("/image/resize/{filename}")
def resize_image(filename: str, settings: ResizeInput):
    """
    Redimensionar una imatge/vídeo
    """
    payload = {"filename": filename, "width": settings.width, "height": settings.height}
    try:
        response = requests.post(f"http://ffmpeg:9000/image/resize/{filename}", json={"width": settings.width, "height": settings.height})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")

# BW Hard Compression (utilitza l'altre Docker amb FFMPEG)
@app.post("/image/bw-compression/{filename}")
def compress_bw(filename: str):
    """
    Convertir a blanc i negre i comprimir al màxim (qscale 31)
    """
    payload = {"filename": filename}
    try:
        response = requests.post(f"http://ffmpeg:9000/image/bw-compression/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")