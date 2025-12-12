import unittest
import numpy as np
import os
from main import DCT_Converter, DWT_Converter, serpentine_logic, run_length_encoding_logic

class TestMultimediaMethods(unittest.TestCase):

    #TEST 1: Serpentine 
    def test_serpentine_logic(self):
        print("\nTesting Serpentine...")
        matrix = [
            [1, 2, 6],
            [3, 5, 7],
            [4, 8, 9]
        ]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = serpentine_logic(matrix)
        self.assertEqual(result, expected)

    #TEST 2: RLE
    def test_rle_logic(self):
        print("\nTesting RLE...")
        data = [10, 20, 0, 0, 0, 0, 5, 0, 0]
        expected = [10, 20, 0, 4, 5, 0, 2]
        self.assertEqual(run_length_encoding_logic(data), expected)

    #TEST 3: DCT Reversibility
    def test_dct_reversibility(self):
        print("\nTesting DCT Reversibility...")
        dct = DCT_Converter(size=8)
        block = np.random.randint(0, 255, (8, 8))
        
        coeffs = dct.perform_DCT(block)
        recovered = dct.perform_IDCT(coeffs)
        
        mse = np.mean((block - recovered) ** 2)
        # Acceptem un error molt petit degut a decimals
        self.assertLess(mse, 0.001, "L'error (MSE) de la DCT és massa gran!")

    #TEST 4: DWT Reversibility
    def test_dwt_reversibility(self):
        print("\nTesting DWT Reversibility...")
        dwt = DWT_Converter()
        block = np.array([
            [100, 100, 50, 50],
            [100, 100, 50, 50],
            [20,  20,  10, 10],
            [20,  20,  10, 10]
        ])
        
        coeffs = dwt.perform_DWT(block)
        recovered = dwt.perform_IDWT(coeffs)
        
        mse = np.mean((block - recovered) ** 2)
        self.assertLess(mse, 0.001, "L'error (MSE) de la DWT és massa gran!")

if __name__ == '__main__':
    unittest.main()