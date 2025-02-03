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
        
# Creación de la ventana principal
root = tk.Tk()

# Configuración de la ventana principal
root.title("Calculadora de IMC")
root.geometry("800x600+100+100")
root.configure(bg="#117ED9")

# Configuración de los Frames
# Frame para el título
frame_titulo = tk.Frame(root, bg="#CFD911", height=50)
frame_titulo.pack(fill='x', expand=True, padx=10, pady=10)

# Título de la app
titulo = tk.Label(frame_titulo, text="Vamos a calcular tu IMC y composición corporal", font=("Helvetica", 16, "bold"), bg="#CFD911", fg="#344859")
titulo.pack(pady=10)

# Frame para alojar el peso y la altura
frame_entradas = tk.Frame(root, bg="#344859", height=70)
frame_entradas.pack(fill='x', expand=True, padx=10, pady=10, anchor="center")

# SubFrame para poder centrar los elementos en horizontal
subframe_entrada = tk.Frame(frame_entradas, bg="#344859")
subframe_entrada.pack()

# Peso
label_peso = tk.Label(subframe_entrada, text="Peso (kg):", font=("Verdana", 14, "bold"), bg="#344859", fg="#D9B311")
label_peso.pack(side=tk.LEFT, padx=10,pady=10, anchor="center")
peso = tk.StringVar()
entry_peso = tk.Entry(subframe_entrada, textvariable=peso, bg="lightyellow", fg="#363884", font=("Verdana", 14), width=10, justify="center")
entry_peso.pack(side=tk.LEFT, padx=10,pady=10, anchor="center")

# Altura
label_altura = tk.Label(subframe_entrada, text="Altura (cm):", font=("Verdana", 14, "bold"), bg="#344859", fg="#D9B311")
label_altura.pack(side=tk.LEFT, padx=10,pady=10, anchor="center")
altura = tk.StringVar()
entry_altura = tk.Entry(subframe_entrada, textvariable=altura, bg="lightyellow", fg="#363884", font=("Verdana", 14), width=10, justify="center")
entry_altura.pack(side=tk.LEFT, padx=10,pady=10, anchor="center")

# Centramos las entradas en el Frame
subframe_entrada.pack(anchor=tk.CENTER)

# Frame Principal para el Sexo
frame_intermedio = tk.Frame(root,bg="#8472ED")
frame_intermedio.pack(fill="x",expand="True", padx=10, pady=10)

# Frame para el Sexo
frame_sexo = tk.Frame(frame_intermedio, bg="")
frame_sexo.pack()
#Creamos la Etiqueta
label_sexo = tk.Label(frame_sexo, text="Sexo", font=("Verdana", 14, "bold"), width=10, justify="center", bg="#8472ED", fg="#ED7286")
label_sexo.pack(side="left",padx=10,pady=10)
# Variable para almacenar el resultado de la selección 'Sexo'
var_sexo = tk.StringVar(value="Hombre")
# Creación de los Radiobuttons
tk.Radiobutton(frame_sexo, text="Hombre", variable=var_sexo, value="Hombre", bg="#8472ED", highlightbackground="#8472ED", font=("Verdana", 14, "bold"),highlightcolor="#AC72ED").pack(side="left",padx=10,pady=10)
tk.Radiobutton(frame_sexo, text="Mujer", variable=var_sexo, value="Mujer",bg="#8472ED", highlightbackground="#8472ED", font=("Verdana", 14, "bold"),highlightcolor="#AC72ED").pack(side="left", padx=10,pady=10)   

frame_sexo.pack(anchor="center")

# Frame para mostrar la imagen
frame_imagen = tk.Frame(root)
frame_imagen.pack(pady=10)

# Panel para mostrar la imagen
panel = tk.Label(frame_imagen)
panel.pack()

# Frame para el botón
frame_boton = tk.Frame(root)
frame_boton.pack(pady=10)

# Botón para calcular el IMC
tk.Button(frame_boton, text="Calcular IMC", command=calcular_imc).pack()

root.mainloop()