import json
import tkinter as tk
from tkinter import ttk

# Cargar datos desde el archivo JSON
with open("assets/titulaciones.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extraer datos únicos para los filtros
universidades = sorted(set(item["Universidad"] for item in data))
facultades = sorted(set(item["Facultad"] for item in data))

# Crear la ventana principal
root = tk.Tk()
root.title("Buscador de Titulaciones")

# Variables para almacenar los filtros y el checkbox
titulacion_var = tk.StringVar()
universidad_var = tk.StringVar(value="Todas")
facultad_var = tk.StringVar(value="Todas")
mostrar_deportista_var = tk.BooleanVar(value=True)  # Valor inicial True (mostrar nota deportista)

# Función para filtrar y actualizar la lista de titulaciones
def actualizar_lista(*args):
    filtro_texto = titulacion_var.get().lower()
    filtro_uni = universidad_var.get()
    filtro_fac = facultad_var.get()

    # Filtrar datos
    resultados = [
        item["Titulación"]
        for item in data
        if filtro_texto in item["Titulación"].lower() and
        (filtro_uni == "Todas" or item["Universidad"] == filtro_uni) and
        (filtro_fac == "Todas" or item["Facultad"] == filtro_fac)
    ]
    
    # Actualizar Listbox
    listbox_titulaciones.delete(0, tk.END)
    for titulo in resultados:
        listbox_titulaciones.insert(tk.END, titulo)

# Función para mostrar la nota de corte seleccionada (general o deportista)
def mostrar_nota(event):
    seleccion = listbox_titulaciones.get(tk.ACTIVE)
    for item in data:
        if item["Titulación"] == seleccion:
            if mostrar_deportista_var.get():
                resultado.set(f"Nota de Corte General: {item['General']}\nNota de Corte Deportista: {item['Deportista']}")
            else:
                resultado.set(f"Nota de Corte General: {item['General']}")
            return
    resultado.set("No se encontró información.")

# Crear widgets
tk.Label(root, text="Buscar Titulación:").grid(row=0, column=0, sticky="w")
entry_titulacion = ttk.Entry(root, textvariable=titulacion_var, width=50)
entry_titulacion.grid(row=0, column=1, padx=5, pady=5)
entry_titulacion.bind("<KeyRelease>", actualizar_lista)  # Filtra al escribir

tk.Label(root, text="Filtrar por Universidad:").grid(row=1, column=0, sticky="w")
combo_uni = ttk.Combobox(root, textvariable=universidad_var, values=["Todas"] + universidades, state="readonly")
combo_uni.grid(row=1, column=1, padx=5, pady=5)
combo_uni.bind("<<ComboboxSelected>>", actualizar_lista)

tk.Label(root, text="Filtrar por Facultad:").grid(row=2, column=0, sticky="w")
combo_fac = ttk.Combobox(root, textvariable=facultad_var, values=["Todas"] + facultades, state="readonly")
combo_fac.grid(row=2, column=1, padx=5, pady=5)
combo_fac.bind("<<ComboboxSelected>>", actualizar_lista)

listbox_titulaciones = tk.Listbox(root, height=10, width=50)
listbox_titulaciones.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Reemplazamos bind con una nueva función para manejar la selección
def on_select(event):
    # Este evento se dispara tanto al usar las flechas como al hacer clic
    mostrar_nota(event)

listbox_titulaciones.bind("<<ListboxSelect>>", on_select)  # Maneja la selección

# Opción para mostrar o no la nota de deportista
tk.Checkbutton(root, text="Mostrar Nota de Deportista de Élite", variable=mostrar_deportista_var).grid(row=4, column=0, columnspan=2)

resultado = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado, fg="blue")
label_resultado.grid(row=5, column=0, columnspan=2, pady=10)

# Inicializar lista
actualizar_lista()

# Ejecutar la aplicación
root.mainloop()
