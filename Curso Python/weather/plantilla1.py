import tkinter as tk
from PIL import Image, ImageTk

# Función para cargar imágenes dinámicamente en un Label
def cargar_imagen(label, ruta_imagen):
    # Abrir la imagen
    imagen = Image.open(ruta_imagen)
    # Redimensionar la imagen si es necesario (opcional)
    imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
    # Convertir la imagen a formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)
    # Configurar el Label para mostrar la imagen
    label.config(image=imagen_tk)
    label.image = imagen_tk  

# Crear la ventana principal
root = tk.Tk()
root.title("Plantilla 1")
root.geometry("800x800")  # Establecer dimensiones de la ventana (opcional)

# Frame Título
# Crear un marco para el título
frame_titulo = tk.Frame(root, bg="#81C5E6", height=50)
frame_titulo.pack(side="top", fill="x",padx=10,pady=(10,0))  # Alinear verticalmente y ocupar todo el ancho
# Crear una etiqueta dentro del marco
label_titulo = tk.Label(frame_titulo, text="frame_titulo", bg="#81C5E6", fg="#4B5D66", font=("Arial", 16, "bold"))
label_titulo.pack(pady=10)

# Frame Búsqueda de la ciudad
# Crear un marco para la búsqueda de la ciudad
frame_busqueda = tk.Frame(root, bg="#ACE681", height=50)
frame_busqueda.pack(side="top", fill="x", padx=10, pady=(10, 0))  # Alinear verticalmente y ocupar todo el ancho
# Crear una etiqueta dentro del marco
label_busqueda = tk.Label(frame_busqueda, text="frame_busqueda", bg="#ACE681", fg="#4B5D66", font=("Arial", 16, "bold"))
label_busqueda.pack(pady=10)

# Frame Información del clima
# Crear un marco para la información del clima
frame_clima = tk.Frame(root, bg="#DF81E5", height=170)
frame_clima.pack(side="top", fill="x", padx=10, pady=(10, 0))  # Alinear verticalmente arriba y ocupar todo el ancho
frame_clima.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

# Vamos a partir el frame_clima en 2 partes horizontalmente
# Parte 1, situación general del clima: Clouds, Clear, Rain, Snow
frame_clima_general = tk.Frame(frame_clima, bg="#E6B881", width=385, height=150)
frame_clima_general.pack(side="left", fill="both", padx=(10,5), pady=10, expand=True)  # Alinear horizontalmente a la izquierda
frame_clima_general.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

label_clima_general = tk.Label(frame_clima_general, text="frame_clima_general", bg="#E6B881", fg="#4B5D66", font=("Arial", 16, "bold"))
label_clima_general.pack(pady=10)

# Parte 2, descripción del clima
frame_clima_detalle = tk.Frame(frame_clima, bg="#E6B881", width=385, height=150)
frame_clima_detalle.pack(side="left", fill="both", padx=(5,10), pady=10, expand=True)  # Alinear horizontalmente a la derecha
frame_clima_detalle.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

label_clima_descripcion = tk.Label(frame_clima_detalle, text="frame_clima_detalle", bg="#E6B881", fg="#4B5D66", font=("Arial", 16, "bold"))
label_clima_descripcion.pack(pady=10)

# Frame para las temperaturas
# Crear un marco principal para las temperaturas  
frame_temperaturas = tk.Frame(root, bg="#B549E6", height=150)
frame_temperaturas.pack(side="top", fill="x", padx=10, pady=(10, 0))  # Alinear verticalmente arriba y ocupar todo el ancho
frame_temperaturas.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

# Vamos a partir el frame_temperaturas en 4 partes horizontalmente
# Parte 1, temperatura actual
frame_temp_actual = tk.Frame(frame_temperaturas, bg="#E6B881", width=187)
frame_temp_actual.pack(side="left", fill="both", padx=(10,5), pady=10, expand=True)  # Alinear horizontalmente a la izquierda
frame_temp_actual.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
label_temp_actual = tk.Label(frame_temp_actual, text="frame_temp_actual", bg="#E6B881", fg="#4B5D66", font=("Arial", 12, "bold"))
label_temp_actual.pack(pady=10)
# Parte 2, temperatura máxima
frame_temp_max = tk.Frame(frame_temperaturas, bg="#E6B881", width=188)
frame_temp_max.pack(side="left", fill="both", padx=(5,5), pady=10, expand=True)  # Alinear horizontalmente a la derecha
frame_temp_max.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
label_temp_max = tk.Label(frame_temp_max, text="frame_temp_max", bg="#E6B881", fg="#4B5D66", font=("Arial", 12, "bold"))
label_temp_max.pack(pady=10)
# Parte 3, temperatura mínima
frame_temp_min = tk.Frame(frame_temperaturas, bg="#E6B881", width=188)
frame_temp_min.pack(side="left", fill="both", padx=(5,5), pady=10, expand=True)  # Alinear horizontalmente a la izquierda
frame_temp_min.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
label_temp_min = tk.Label(frame_temp_min, text="frame_temp_min", bg="#E6B881", fg="#4B5D66", font=("Arial", 12, "bold"))
label_temp_min.pack(pady=10)
# Parte 4, sensación térmica
frame_temp_sensacion = tk.Frame(frame_temperaturas, bg="#E6B881", width=187)
frame_temp_sensacion.pack(side="right", fill="both", padx=(5,10), pady=10, expand=True)  # Alinear horizontalmente a la derecha
frame_temp_sensacion.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
label_temp_sensacion = tk.Label(frame_temp_sensacion, text="frame_temp_sensacion", bg="#E6B881", fg="#4B5D66", font=("Arial", 12, "bold"))
label_temp_sensacion.pack(pady=10)

# Vamos a crear un Frame para partirlo verticalmente en dos y horizontalmente en 3

# Frame 2x3 para el resto de la información
frame_info = tk.Frame(root, bg="#BEE649", height=240)
frame_info.pack(side="top", fill="x", padx=10, pady=(10, 0))  # Alinear verticalmente arriba y ocupar todo el ancho
frame_info.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

#Frame 1, que vamos a partir en 2 verticalmente
frame_info_1 = tk.Frame(frame_info, bg="#E6B881", width=253, height=220)
frame_info_1.pack(side="left", fill="both", padx=(10,5), pady=10, expand=True)  # Alinear horizontalmente a la izquierda
frame_info_1.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

frame_info_1_1 = tk.Frame(frame_info_1, bg="#49D8E6", width=187, height=95)
frame_info_1_1.pack(side="top", fill="both", padx=10, pady=(10,5), expand=True)  # Alinear horizontalmente a la izquierda
frame_info_1_1.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

frame_info_1_2 = tk.Frame(frame_info_1, bg="#49D8E6", width=187, height=95)
frame_info_1_2.pack(side="top", fill="both", padx=10, pady=(5,10), expand=True)  # Alinear horizontalmente a la izquierda
frame_info_1_2.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

frame_info_2 = tk.Frame(frame_info, bg="#B549E6", width=253, height=220)
frame_info_2.pack(side="left", fill="both", padx=(5,5), pady=10, expand=True)  # Alinear horizontalmente a la derecha
frame_info_2.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
frame_info_2_1 = tk.Frame(frame_info_2, bg="#605466", width=187, height=95)
frame_info_2_1.pack(side="top", fill="both", padx=10, pady=(10,5), expand=True)  # Alinear horizontalmente a la izquierda
frame_info_2_1.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
frame_info_2_2 = tk.Frame(frame_info_2, bg="#605466", width=187, height=95)
frame_info_2_2.pack(side="top", fill="both", padx=10, pady=(5,10), expand=True)  # Alinear horizontalmente a la izquierda
frame_info_2_2.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado

frame_info_3 = tk.Frame(frame_info, bg="#49D8E6", width=253, height=220)
frame_info_3.pack(side="left", fill="both", padx=(5,10), pady=10, expand=True)  # Alinear horizontalmente a la derecha
frame_info_3.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
frame_info_3_1 = tk.Frame(frame_info_3, bg="#E68A49", width=187, height=95)
frame_info_3_1.pack(side="top", fill="both", padx=10, pady=(10,5), expand=True)  # Alinear horizontalmente a la izquierda
frame_info_3_1.pack_propagate(False)  # Evitar que el marco cambie de tamaño según su contenido, dependerá del tamaño especificado
frame_info_3_2 = tk.Frame(frame_info_3, bg="#E68A49", width=187, height=95)
frame_info_3_2.pack(side="top", fill="both", padx=10, pady=(5,10), expand=True)  # Alinear horizontalmente a la izquierda

cargar_imagen(label_temp_actual,'img/temperatura.png')

# Iniciar el bucle principal
root.mainloop()