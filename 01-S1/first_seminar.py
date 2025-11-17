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
