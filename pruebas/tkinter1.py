import tkinter as tk

root = tk.Tk()

root.title("Mi primera ventana")

# Dimensiones de la ventana
ancho_ventana = 800
alto_ventana = 600

# Obtener el tamaño de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular la posición para centrar la ventana
pos_x = (ancho_pantalla - ancho_ventana) // 2
pos_y = (alto_pantalla - alto_ventana) // 2

# Configurar la geometría de la ventana
root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

root.mainloop()