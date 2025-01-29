from PIL import ImageTk, Image

def leer_imagen(ruta, size):
    imagen = Image.open(ruta)
    imagen = imagen.resize(size, Image.ADAPTIVE)
    return ImageTk.PhotoImage(imagen)