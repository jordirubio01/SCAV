import ffmpeg
import os
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
