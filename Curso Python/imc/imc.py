import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

somatotipo_images = {
    "Ectomorfo": "ectomorfo.png",
    "Mesomorfo": "mesomorfo.png",
    "Endomorfo": "endomorfo.png"
}

def calcular_imc():
    try:
        peso = float(entry_peso.get())
        altura = float(entry_altura.get()) / 100  # Convertir cm a metros
        imc = peso / (altura ** 2)
        sexo = var_sexo.get()
        
        if sexo == "Hombre":
            if imc < 20:
                morfologia = "Delgado"
            elif 20 <= imc < 25:
                morfologia = "Normal"
            else:
                morfologia = "Sobrepeso"
        else:
            if imc < 18.5:
                morfologia = "Delgada"
            elif 18.5 <= imc < 24:
                morfologia = "Normal"
            else:
                morfologia = "Sobrepeso"
        
        if imc < 18.5:
            somatotipo = "Ectomorfo"
        elif 18.5 <= imc < 24.9:
            somatotipo = "Mesomorfo"
        else:
            somatotipo = "Endomorfo"
        
        print(f"images/{somatotipo_images[somatotipo]}")
        img = Image.open(f"images/{somatotipo_images[somatotipo]}")
        img = img.resize((150, 150), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img
        
        messagebox.showinfo("Resultado", f"IMC: {imc:.2f}\nMorfología: {morfologia}\nSomatotipo: {somatotipo}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce valores válidos.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró la imagen: {img}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de IMC")

# Crear frames
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10, padx=10)

frame_sexo = tk.Frame(root)
frame_sexo.pack(pady=10)

frame_imagen = tk.Frame(root)
frame_imagen.pack(pady=10)

frame_boton = tk.Frame(root)
frame_boton.pack(pady=10)

# Etiquetas y campos de entrada
tk.Label(frame_entrada, text="Peso (kg):").pack(side=tk.LEFT)
entry_peso = tk.Entry(frame_entrada)
entry_peso.pack(side=tk.LEFT)

tk.Label(frame_entrada, text="Altura (cm):").pack(side=tk.LEFT)
entry_altura = tk.Entry(frame_entrada)
entry_altura.pack(side=tk.LEFT)

tk.Label(frame_sexo, text="Sexo:").pack(side=tk.LEFT)
var_sexo = tk.StringVar(value="Hombre")
tk.Radiobutton(frame_sexo, text="Hombre", variable=var_sexo, value="Hombre").pack(side=tk.LEFT)
tk.Radiobutton(frame_sexo, text="Mujer", variable=var_sexo, value="Mujer").pack(side=tk.LEFT)

# Panel para mostrar la imagen
panel = tk.Label(frame_imagen)
panel.pack()

# Botón para calcular el IMC
tk.Button(frame_boton, text="Calcular IMC", command=calcular_imc).pack()

# Iniciar el bucle principal de la interfaz
root.mainloop()