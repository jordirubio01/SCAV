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

class MatrixInput(BaseModel):
    matrix: List[List[float]]

class ResizeInput(BaseModel):
    width: int
    height: int

class ChromaInput(BaseModel):
    subsampling: str  # p.e. "yuv420p", "yuv422p", "yuv444p"

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

#Serpentine
def serpentine_logic(matrix_in):
    matrix = np.array(matrix_in)
    rows, cols = matrix.shape
    solution = [[] for i in range(rows + cols - 1)]

    for i in range(rows):
        for j in range(cols):
            sum_idx = i + j
            if sum_idx % 2 == 0:
                solution[sum_idx].insert(0, matrix[i][j])
            else:
                solution[sum_idx].append(matrix[i][j])
    return [item for sublist in solution for item in sublist]

#DCT Class
class DCT_Converter:
    def __init__(self, size=8):
        self.N = size
        self.T = self._create_basis_matrix(self.N)

    def _create_basis_matrix(self, N):
        T = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == 0:
                    T[i, j] = np.sqrt(1 / N)
                else:
                    T[i, j] = np.sqrt(2 / N) * np.cos(((2 * j + 1) * i * np.pi) / (2 * N))
        return T

    def perform_DCT(self, pixel_block):
        # Centrem valors restant 128
        centered_block = pixel_block - 128
        return np.dot(np.dot(self.T, centered_block), self.T.T)

    def perform_IDCT(self, dct_block):
        reconstructed = np.dot(np.dot(self.T.T, dct_block), self.T)
        return reconstructed + 128

#DWT Class
class DWT_Converter:
    def perform_DWT(self, image_matrix):
        data = image_matrix.astype(float)
        rows, cols = data.shape
        
        # Rows
        evens_row, odds_row = data[:, 0::2], data[:, 1::2]
        L_row, H_row = (evens_row + odds_row) / 2, (evens_row - odds_row) / 2
        processed_rows = np.hstack((L_row, H_row))

        # Columns
        evens_col, odds_col = processed_rows[0::2, :], processed_rows[1::2, :]
        L_col, H_col = (evens_col + odds_col) / 2, (evens_col - odds_col) / 2
        
        return np.vstack((L_col, H_col))

    def perform_IDWT(self, dwt_matrix):
        rows, cols = dwt_matrix.shape
        half_rows, half_cols = rows // 2, cols // 2

        # Inverse Columnes
        L_col, H_col = dwt_matrix[:half_rows, :], dwt_matrix[half_rows:, :]
        evens_col, odds_col = L_col + H_col, L_col - H_col
        
        reconstructed_cols = np.zeros((rows, cols))
        reconstructed_cols[0::2, :] = evens_col
        reconstructed_cols[1::2, :] = odds_col

        # Inverse Rows
        L_row, H_row = reconstructed_cols[:, :half_cols], reconstructed_cols[:, half_cols:]
        evens_row, odds_row = L_row + H_row, L_row - H_row

        final_image = np.zeros((rows, cols))
        final_image[:, 0::2] = evens_row
        final_image[:, 1::2] = odds_row
        return final_image

# Api endponts

@app.get("/")
def read_root():
    return {"message": "API Seminari 2 Integrada amb Docker i FFMPEG (separats)"}


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

#Serpentine Endpoint
@app.post("/algorithm/serpentine")
def perform_serpentine(payload: MatrixInput):
    """
    Retorna l'escaneig en Zig-Zag d'una matriu NxM.
    """
    try:
        result = serpentine_logic(payload.matrix)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#DCT Endpoint
@app.post("/algorithm/dct")
def perform_dct(payload: MatrixInput):
    """
    Aplica la transformació DCT a un bloc (idealment 8x8).
    """
    try:
        matrix = np.array(payload.matrix)
        converter = DCT_Converter(size=matrix.shape[0])
        dct_coeffs = converter.perform_DCT(matrix)
        return {"dct_coefficients": dct_coeffs.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#DWT Endpoint
@app.post("/algorithm/dwt")
def perform_dwt(payload: MatrixInput):
    """
    Aplica la transformació DWT (Haar) a una matriu.
    """
    try:
        matrix = np.array(payload.matrix)
        converter = DWT_Converter()
        dwt_coeffs = converter.perform_DWT(matrix)
        return {"dwt_coefficients": dwt_coeffs.tolist()}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Resize Image (utilitza l'altre Docker amb FFMPEG)
@app.post("/image/resize/{filename}")
def resize_image(filename: str, settings: ResizeInput):
    """
    Endpoint API que crida al servei FFMPEG per redimensionar una imatge/vídeo
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
    Endpoint API que crida al servei FFMPEG per convertir a blanc i negre i comprimir al màxim (qscale 31)
    """
    payload = {"filename": filename}
    try:
        response = requests.post(f"http://ffmpeg:9000/image/bw-compression/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Canviar Resolució Vídeo (utilitza l'altre Docker amb FFMPEG)
@app.post("/video/change-resolution/{filename}")
def change_resolution(filename: str, settings: ResizeInput):
    """
    Endpoint API que crida al servei FFMPEG per canviar la resolució d'un vídeo
    """
    try:
        response = requests.post(
            f"http://ffmpeg:9000/video/change-resolution/{filename}",
            json={"width": settings.width, "height": settings.height}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Canviar Chroma Subsampling (utilitza l'altre Docker amb FFMPEG)
@app.post("/video/chroma-subsampling/{filename}")
def change_chroma_subsampling(filename: str, settings: ChromaInput):
    """
    Endpoint API que crida al servei FFMPEG per modificar el chroma subsampling.
    """
    try:
        response = requests.post(
            f"http://ffmpeg:9000/video/chroma-subsampling/{filename}",
            json={"subsampling": settings.subsampling}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Informació del Vídeo (utilitza l'altre Docker amb FFMPEG)
@app.get("/video/info/{filename}")
def get_video_info(filename: str):
    """
    Endpoint API que crida al servei FFMPEG per obtenir informació del vídeo
    """
    try:
        response = requests.get(f"http://ffmpeg:9000/video/info/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Big Buck Bunny Container (utilitza l'altre Docker amb FFMPEG)
@app.post("/video/create-bbb-container/{filename}")
def create_bbb_container(filename: str):
    """
    Endpoint API que crida al servei FFMPEG per crear un contenidor MP4 amb:
    - Vídeo Big Buck Bunny retallat a 20s
    - Àudio AAC mono
    - Àudio MP3 stereo amb bitrate baix
    - Àudio AC3
    """
    try:
        response = requests.post(f"http://ffmpeg:9000/video/create-bbb-container/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Nombre de Tracks del Contenidor (utilitza l'altre Docker amb FFMPEG)
@app.get("/video/tracks/{filename}")
def get_video_tracks(filename: str):
    """
    Endpoint API que crida al servei FFMPEG per comptar quantes pistes té un contenidor MP4.
    """
    try:
        response = requests.get(f"http://ffmpeg:9000/video/tracks/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Mostrar Macroblocks i Motion Vectors (utilitza l'altre Docker amb FFMPEG)
@app.post("/video/show-motion/{filename}")
def show_motion_vectors(filename: str):
    """
    Endpoint API que crida al servei FFMPEG per generar un vídeo amb macroblocks i vectors de moviment visibles.
    """
    try:
        response = requests.post(f"http://ffmpeg:9000/video/show-motion/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")
    
# Mostrar Histograma YUV (utilitza l'altre Docker amb FFMPEG)
@app.post("/video/yuv-histogram/{filename}")
def show_yuv_histogram(filename: str):
    """
    Endpoint API que crida al servei FFMPEG per generar un vídeo amb el histograma YUV visible.
    """
    try:
        response = requests.post(f"http://ffmpeg:9000/video/yuv-histogram/{filename}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cridant el servei ffmpeg: {str(e)}")