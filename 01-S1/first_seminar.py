import ffmpeg
import os
from PIL import Image
import numpy as np
# 1st TASK
class ColorTranslator:
    # Convert from RGB scale to YUV
    def RGBtoYUV(self, R, G, B):
        Y =  0.257 * R + 0.504 * G + 0.098 * B +  16
        U = -0.148 * R - 0.291 * G + 0.439 * B + 128
        V =  0.439 * R - 0.368 * G - 0.071 * B + 128
        return Y, U, V

    # Convert from YUV scale to RGB
    def YUVtoRGB(self, Y, U, V):
        R = 1.164 * (Y - 16) + 1.596 * (V - 128)
        G = 1.164 * (Y - 16) - 0.813 * (V - 128) - 0.391 * (U - 128)
        B = 1.164 * (Y - 16) + 2.018 * (U - 128)
        return R, G, B

converter = ColorTranslator()
R=194
G=61
B=92
Y, U, V = converter.RGBtoYUV(R, G, B)
print(f"RGB: {R}, {G}, {B}; YUV: {Y}, {U}, {V}.")

R, G, B = converter.YUVtoRGB(Y, U, V)
print(f"YUV: {Y}, {U}, {V}; RGB: {R}, {G}, {B}.")
#TODO: Implement it with the cmd or reading .txt file

#2nd TASK
#Foto from Halyna Chemerys https://unsplash.com/es/fotos/un-grupo-de-caballos-u3LdAMV_CIo?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink
def resizeImageOS(filename, output_width, output_height):
    os.system(f"ffmpeg -i {filename}.jpg -vf scale={output_width}:{output_height} horses_{output_width}_{output_height}.jpg")

filename="horses"
print(os.path.exists(filename))
sizes = [[1000,1000], [500,500], [50,50], [100,100]]
for size in sizes:
    resizeImageOS(filename, size[0], size[1])
#TODO: Improve the function if possible (maybe without using the os command)

#2nd TASK with ffmpeg
#Code example found in https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md
#Scale shell command --> ffmpeg -i input_image.jpg -vf scale=500:500 output_image.jpg  (vb = video filter)

def resizeImage_ffmpeg(filename, output_width, output_height):
    (
        ffmpeg
        .input(f"{filename}.jpg")
        .filter("scale", output_width, output_height)
        .output(f"horses_{output_width}_{output_height}_ffmpeg.jpg")
        .run()
    )

filename="horses"
sizes = [[1000,1000], [500,500], [50,50], [100,100]]
for size in sizes:
    resizeImage_ffmpeg(filename, size[0], size[1])

#3rd Task
def serpentine(matrix):

    rows, cols = matrix.shape
    solution = [[] for i in range(rows + cols - 1)]

    for i in range(rows):
        for j in range(cols):
            sum_idx = i + j
            if sum_idx % 2 == 0:
                # Si la suma d'índexs és parella, afegim al principi (pujada)
                solution[sum_idx].insert(0, matrix[i][j])
            else:
                # Si és senar, afegim al final (baixada)
                solution[sum_idx].append(matrix[i][j])

    # Aplanar la llista de llistes en un sol vector lineal
    return [item for sublist in solution for item in sublist]


# Simulem llegir un bloc de 8x8 (com es fa a JPEG) podem fer servir una imatge real tenint en compte que JPEG treballa en blocs de 8x8
filename = "horses.jpg" 
# Convertim a gris per simplificar l'exemple (valors 0-255)
img = Image.open(filename).convert('L') 
img_array = np.array(img)

# Agafem només el primer bloc de 8x8 píxels de la imatge
# (Tal com deiem a teoria: "used to convert the 8x8 DCT spectrum")
block_8x8 = img_array[0:8, 0:8] 

print("--- Bloc original 8x8 (Bytes/Pixels) ---")
print(block_8x8)

serpentine_bytes = serpentine(block_8x8)

print("\n--- Sequencia Serpentine (Zig-Zag) ---")
print(serpentine_bytes)
print(f"Total elements: {len(serpentine_bytes)}") # Hauria de ser 64

#4th Task
def compress_bw_hardest(input_filename):

    output_filename = f"bw_compressed_{input_filename}"
    
    try:
        (
            ffmpeg
            .input(input_filename)
            .filter('hue', s=0)       # Filtre: Saturation = 0 (Blanc i Negre)
            .output(output_filename, **{'qscale:v': 31}) # qscale:v 31 és la pitjor qualitat (màxima compressió)
            .overwrite_output()
            .run()          
        )
    except ffmpeg.Error as e:
        print("Hi ha hagut un error amb FFmpeg:", e)
        return

    # Comentari de resultats (Comparació de mides)
    if os.path.exists(output_filename):
        original_size = os.path.getsize(input_filename)
        compressed_size = os.path.getsize(output_filename)
        compression_ratio = (1 - (compressed_size / original_size)) * 100

filename = "horses.jpg" 
compress_bw_hardest(filename)   

#5th Task
def run_length_encoding(data):
    #Substitueix les seqüències de zeros per un parell (0, count).

    encoded = []
    i = 0

    while i < len(data):
        # Cas 1: El valor NO és zero
        if data[i] != 0:
            encoded.append(data[i])
            i += 1
        
        # Cas 2: El valor ÉS zero
        else:
            count = 0
            # Comptem quants zeros seguits hi ha
            while i < len(data) and data[i] == 0:
                count += 1
                i += 1
        
            encoded.append(0)
            encoded.append(count)

    return encoded


#Vector simulat que s'assembli al resultat d'una DCT quantitzada --> Molta informació al principi, molts zeros al final
sim_vector = [
    25, 12, 10, 0, 0, 0, 0, 5,  
    0, 0, 2, 0,                 
    0, 0, 0, 0, 0, 0, 0, 0,     
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
]

rle_result = run_length_encoding(sim_vector)
print("----5th Task----")
print(f"Sortida (Encoded):    {rle_result}")
print(f"Mida comprimida: {len(rle_result)} elements")

