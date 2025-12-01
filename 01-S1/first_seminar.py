import ffmpeg
import os
from PIL import Image
import numpy as np
import unittest
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
    output_name = f"horses_{output_width}_{output_height}_ffmpeg.jpg"
    (
        ffmpeg
        .input(f"{filename}.jpg")
        .filter("scale", output_width, output_height)
        .output(output_name)
        .overwrite_output()
        .run(quiet=True)
    )
    return output_name

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

    # Aplanar la llista de llistes en una sola
    return [item for sublist in solution for item in sublist]


# Simulem llegir un bloc de 8x8 (com es fa a JPEG) podem fer servir una imatge real tenint en compte que JPEG treballa en blocs de 8x8
filename = "horses.jpg" 
# Convertim a gris per simplificar-ho (valors 0-255)
img = Image.open(filename).convert('L') 
img_array = np.array(img)

# Agafem només el primer bloc de 8x8 píxels de la imatge --> Tal com deiem a teoria: "used to convert the 8x8 DCT spectrum"
block_8x8 = img_array[0:8, 0:8] 

print("----3rd Task----")
print("--- Bloc original 8x8 (Bytes/Pixels) ---")
print(block_8x8)

serpentine_bytes = serpentine(block_8x8)

print("\n--- Sequencia Serpentine (Zig-Zag) ---")
print(serpentine_bytes)
print(f"Total elements: {len(serpentine_bytes)}") # Hauria de ser 64 per anar bé

#4th Task
def compress_bw_hardest(input_filename):
    output_name = f"bw_compressed_{input_filename}"
    try:
        (
            ffmpeg
            .input(input_filename)
            .filter('hue', s=0)       # Filtre: Saturation = 0 (blanc i negre)
            .output(output_name, **{'qscale:v': 31}) # qscale:v 31 és la pitjor qualitat, és a dir, màxima compressió
            .overwrite_output()
            .run()          
        )
        return output_name
    except ffmpeg.Error as e:
        print("Hi ha hagut un error amb FFmpeg:", e)
        return

    # Comparació de mides
    if os.path.exists(output_name):
        original_size = os.path.getsize(input_filename)
        compressed_size = os.path.getsize(output_name)
        compression_ratio = (1 - (compressed_size / original_size)) * 100

filename = "horses.jpg" 
compress_bw_hardest(filename)   

#5th Task
def run_length_encoding(data):
    #La funció substitueisix les seqüències de zeros per un parell (0, count).

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

# 6th Task: DCT Converter Class
class DCT_Converter:
    def __init__(self, size=8):
        self.N = size
        # We precompute the Transformation Matrix (T) on initialization
        # so we don't have to recalculate cosines every time.
        self.T = self._create_basis_matrix(self.N)

    def _create_basis_matrix(self, N):
        # Create the standard JPEG DCT basis matrix
        T = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == 0:
                    # Alpha for row 0
                    T[i, j] = np.sqrt(1 / N)
                else:
                    # Alpha for other rows
                    T[i, j] = np.sqrt(2 / N) * np.cos(((2 * j + 1) * i * np.pi) / (2 * N))
        return T

    def perform_DCT(self, pixel_block):
        """
        Applies Forward DCT: Y = T * X * T'
        Input: 2D numpy array (Spatial Domain)
        Output: 2D numpy array (Frequency Domain)
        """
        # We subtract 128 to center values around 0 (standard JPEG practice)
        centered_block = pixel_block - 128
        return np.dot(np.dot(self.T, centered_block), self.T.T)

    def perform_IDCT(self, dct_block):
        """
        Applies Inverse DCT: X = T' * Y * T
        Input: 2D numpy array (Frequency Domain)
        Output: 2D numpy array (Spatial Domain)
        """
        reconstructed = np.dot(np.dot(self.T.T, dct_block), self.T)
        # Add 128 back
        return reconstructed + 128

# --- TESTING THE CLASS ---

print("\n---- 6th Task: DCT Class Test ----")

#Initialize the converter
dct_machine = DCT_Converter(size=8)

#Use the 'block_8x8' we extracted in Task 3 (Horses)
# Note: Ensure block_8x8 is defined from the previous code execution
# If running standalone, uncomment the line below:
# block_8x8 = np.random.randint(0, 255, (8,8)) 

print("Original Block (Top-Left 4x4 shown):")
print(block_8x8[:4, :4])

#Apply Forward DCT
dct_coefficients = dct_machine.perform_DCT(block_8x8)
print("\nDCT Coefficients (Top-Left 4x4 shown):")
print("Note the DC coefficient (0,0) is usually the largest.")
print(np.round(dct_coefficients[:4, :4], 1))

#Apply Inverse DCT (IDCT)
recovered_block = dct_machine.perform_IDCT(dct_coefficients)
print("\nReconstructed Block (Top-Left 4x4 shown):")
print(np.round(recovered_block[:4, :4]))

#Check if they are similar
error = np.mean((block_8x8 - recovered_block) ** 2)
print(f"\nMean Squared Error between original and reconstructed: {error:.5f}")


#7th Task
class DWT_Converter:
    
    def __init__(self):
        # We don't need initialization parameters for a standard Haar transform
        pass

    def perform_DWT(self, image_matrix):
        """
        Applies a single-level 2D Haar Wavelet Transform.
        1. Applies 1D DWT to Rows.
        2. Applies 1D DWT to Columns.
        """
        data = image_matrix.astype(float)
        rows, cols = data.shape
        
        # We need even dimensions for this simple implementation
        if rows % 2 != 0 or cols % 2 != 0:
            raise ValueError("Image dimensions must be even for this simple DWT.")

        # --- STEP 1: Process Rows ---
        # We split the image into even columns and odd columns
        # evens = columns 0, 2, 4... | odds = columns 1, 3, 5...
        evens_row = data[:, 0::2]
        odds_row  = data[:, 1::2]

        # Haar Logic: 
        # Low Frequency (L) = Average (or Sum)
        # High Frequency (H) = Difference
        L_row = (evens_row + odds_row) / 2
        H_row = (evens_row - odds_row) / 2

        # Combine them horizontally: [ L | H ]
        processed_rows = np.hstack((L_row, H_row))

        # --- STEP 2: Process Columns ---
        # Now we apply the same logic to the columns of the result
        evens_col = processed_rows[0::2, :]
        odds_col  = processed_rows[1::2, :]

        L_col = (evens_col + odds_col) / 2
        H_col = (evens_col - odds_col) / 2

        # Combine them vertically:
        # [ LL ]
        # [ HH ]
        # Note: In standard 2D DWT, the result is usually organized as:
        # [ LL | HL ]
        # [ LH | HH ]
        # The math here produces that quadrant structure naturally.
        
        dwt_result = np.vstack((L_col, H_col))
        
        return dwt_result

    def perform_IDCT(self, dwt_matrix):
        """
        Applies Inverse DWT (Reconstructs the image).
        Reverse the operations: Columns first, then Rows.
        """
        rows, cols = dwt_matrix.shape
        half_rows = rows // 2
        half_cols = cols // 2

        # --- STEP 1: Inverse Columns ---
        # Split top (Approximation) and bottom (Detail)
        # Recall we stacked them vertically in forward pass
        L_col = dwt_matrix[:half_rows, :]
        H_col = dwt_matrix[half_rows:, :]

        # Inverse Haar Logic:
        # Even = L + H
        # Odd  = L - H
        evens_col = L_col + H_col
        odds_col  = L_col - H_col

        # Interleave them back together
        reconstructed_cols = np.zeros((rows, cols))
        reconstructed_cols[0::2, :] = evens_col
        reconstructed_cols[1::2, :] = odds_col

        # --- STEP 2: Inverse Rows ---
        # Now split left and right
        L_row = reconstructed_cols[:, :half_cols]
        H_row = reconstructed_cols[:, half_cols:]

        evens_row = L_row + H_row
        odds_row  = L_row - H_row

        final_image = np.zeros((rows, cols))
        final_image[:, 0::2] = evens_row
        final_image[:, 1::2] = odds_row

        return final_image

print("\n---- 7th Task ----")

dwt_machine = DWT_Converter()

# Using the 'block_8x8' from your previous code (Horses)
# Or creating a new one if running standalone
# block_8x8 = np.array(...) 

print("Original Block:")
print(block_8x8[:4, :4])

# 1. Forward DWT
dwt_coeffs = dwt_machine.perform_DWT(block_8x8)

print("\nDWT Coefficients:")
print(np.round(dwt_coeffs, 1))

# 2. Inverse DWT
recovered_img = dwt_machine.perform_IDCT(dwt_coeffs)

print("\nReconstructed Block (Top-Left 4x4 shown):")
print(np.round(recovered_img[:4, :4]))

# 3. Check Error
error = np.mean((block_8x8 - recovered_img) ** 2)
print(f"\nMean Squared Error: {error:.5f}")

#8th Task: Unit Tests
class TestMultimediaMethods(unittest.TestCase):

    def setUp(self):
        # Aquest mètode s'executa automàticament ABANS de cada test.
        # Creem una imatge "dummy" per no dependre de si tens 'horses.jpg' o no.
        self.test_img_name = "test_dummy"
        # Creem una imatge vermella de 100x100
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(f"{self.test_img_name}.jpg")

    def tearDown(self):
        # Aquest mètode s'executa automàticament DESPRÉS de cada test.
        # Esborrem els fitxers creats per deixar la carpeta neta.
        if os.path.exists(f"{self.test_img_name}.jpg"):
            os.remove(f"{self.test_img_name}.jpg")
        
        # Neteja extra dels fitxers de sortida generats pels tests
        # (Busquem fitxers que comencin per 'test_dummy' o 'bw_compressed_test_dummy')
        for f in os.listdir():
            if self.test_img_name in f and f.endswith(".jpg"):
                try:
                    os.remove(f)
                except:
                    pass

    # --- TEST 1: ColorTranslator ---
    def test_color_translator_roundtrip(self):
        converter = ColorTranslator()
        r, g, b = 100, 150, 200
        y, u, v = converter.RGBtoYUV(r, g, b)
        r_out, g_out, b_out = converter.YUVtoRGB(y, u, v)
        
        # Comprovem que el resultat és gairebé idèntic a l'entrada
        self.assertAlmostEqual(r, r_out, delta=1)
        self.assertAlmostEqual(g, g_out, delta=1)
        self.assertAlmostEqual(b, b_out, delta=1)

    # --- TEST 2: Resize (FFmpeg) ---
    def test_resize_ffmpeg(self):
        # Cridem a la funció amb la nostra imatge dummy
        output_file = resizeImage_ffmpeg(self.test_img_name, 50, 50)
        
        # Comprovem 1: Que la funció retorni un nom (no None)
        self.assertIsNotNone(output_file, "La funció resize hauria de retornar el nom del fitxer")
        # Comprovem 2: Que el fitxer realment existeixi al disc
        self.assertTrue(os.path.exists(output_file), "El fitxer redimensionat no s'ha creat")

    # --- TEST 3: Serpentine ---
    def test_serpentine_logic(self):
        # Matriu simple 3x3
        matrix = np.array([
            [1, 2, 6],
            [3, 5, 7],
            [4, 8, 9]
        ])
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = serpentine(matrix)
        self.assertEqual(result, expected, "L'algorisme Serpentine no ha ordenat bé")

    # --- TEST 4: Compression ---
    def test_compression_bw(self):
        output_file = compress_bw_hardest(f"{self.test_img_name}.jpg")
        
        self.assertIsNotNone(output_file)
        self.assertTrue(os.path.exists(output_file), "El fitxer comprimit no s'ha creat")
        self.assertTrue(os.path.getsize(output_file) > 0)

    # --- TEST 5: Run Length Encoding ---
    def test_rle_logic(self):
        raw_data = [10, 20, 0, 0, 0, 0, 5, 0, 0]
        expected = [10, 20, 0, 4, 5, 0, 2]
        self.assertEqual(run_length_encoding(raw_data), expected)

    # --- TEST 6: DCT Reversibility ---
    def test_dct_error(self):
        dct = DCT_Converter(size=8)
        block = np.random.randint(0, 255, (8, 8))
        
        coeffs = dct.perform_DCT(block)
        recovered = dct.perform_IDCT(coeffs)
        
        mse = np.mean((block - recovered) ** 2)
        # Acceptem un error molt petit (per culpa dels decimals flotants)
        self.assertLess(mse, 0.001, "L'error (MSE) de la DCT és massa gran!")

    # --- TEST 7: DWT Reversibility ---
    def test_dwt_error(self):
        dwt = DWT_Converter()
        block = np.array([
            [100, 100, 50, 50],
            [100, 100, 50, 50],
            [20,  20,  10, 10],
            [20,  20,  10, 10]
        ])
        
        coeffs = dwt.perform_DWT(block)
        recovered = dwt.perform_IDCT(coeffs)
        
        mse = np.mean((block - recovered) ** 2)
        self.assertLess(mse, 0.001, "L'error (MSE) de la DWT és massa gran!")

if __name__ == '__main__':
    # Executa els tests i mostra el resultat
    print("\n\n========================================")
    print("EXECUTANT TESTS UNITARIS (TASCA 8)")
    print("========================================")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)