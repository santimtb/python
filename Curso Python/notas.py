import customtkinter as ctk

# Configurar apariencia y tema
ctk.set_appearance_mode("light")  # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Tema de colores

# Crear la ventana principal
ventana_principal = ctk.CTk()
ventana_principal.geometry("800x600")
ventana_principal.title("Simulador EBAU")

# Frame para la Nota Media de Bachillerato
frame_bachiller = ctk.CTkFrame(ventana_principal)
frame_bachiller.pack(pady=(10,5), padx=10, fill="x")

ctk.CTkLabel(frame_bachiller, text="Nota Media de Bachillerato:", font=("Arial", 14, "bold")).pack(pady=(5,0))
entry1 = ctk.CTkEntry(frame_bachiller, placeholder_text="Nota media de bachiller...", justify="center")
entry1.pack(pady=10)

# Frame central
frame_central = ctk.CTkFrame(ventana_principal)
frame_central.pack(pady=(5,5), padx=10, fill="x")

# Frame para la Fase Obligatoria
frame_fase_obligatoria = ctk.CTkFrame(frame_central, width=400)
frame_fase_obligatoria.pack(side="left", pady=(10,10), padx=(10,5), fill="both", expand=True)

titulo = ctk.CTkLabel(frame_fase_obligatoria, text="Fase Obligatoria", font=("Arial", 14, "bold"), anchor="center")
titulo.pack(fill="x", padx=10, pady=(5, 0))  

fase_general = ("Castellano: lengua y literatura", "Valenciano: lengua i literaura", "Lengua Extranjera", "Historia de España","Matemáticas")

entries = []  # Lista para almacenar los entry
for i in range(2, 7):  # Asignaturas 2 a 6
    ctk.CTkLabel(frame_fase_obligatoria, text=f"{fase_general[i-2]}:").pack(pady=5)
    entry = ctk.CTkEntry(frame_fase_obligatoria, placeholder_text=f"Nota {fase_general[i-2]}", justify="center")
    entry.pack(pady=5)
    entries.append(entry)

# Frame para la Fase Voluntaria
frame_fase_voluntaria = ctk.CTkFrame(frame_central, width=400)
frame_fase_voluntaria.pack(side="left", pady=(10,10), padx=(5,10), fill="both", expand=True)
titulo2 = ctk.CTkLabel(frame_fase_voluntaria, text="Fase Voluntaria", font=("Arial", 14, "bold"), anchor="center")
titulo2.pack(fill="x", padx=10, pady=(5, 0))  
#OPTATIVA 1
# Frame para la Optativa 1
frame_optativa1 = ctk.CTkFrame(frame_fase_voluntaria)
frame_optativa1.pack(pady=10, padx=10, fill="x", expand=True)
ctk.CTkLabel(frame_optativa1, text="Optativa 1").pack(pady=(5,0))
entry6 = ctk.CTkEntry(frame_optativa1, placeholder_text="Nota optativa 1...")
entry6.pack(pady=5)
# Variable para almacenar la selección del RadioButton Ponderación 1
poneracion1 = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
# Frame para agrupar los botones de Optativa 1
frame_radio1 = ctk.CTkFrame(frame_optativa1)
frame_radio1.pack(pady=10, padx=10, fill="x")
# Etiqueta
ctk.CTkLabel(frame_radio1, text="Ponderación:").pack(pady=5)
# RadioButtons
radio1 = ctk.CTkRadioButton(frame_radio1, text=" 0.2", variable=poneracion1, value=0.2)
radio1.pack(side="left",expand=True, anchor="e",pady=5)
radio2 = ctk.CTkRadioButton(frame_radio1, text=" 0.1", variable=poneracion1, value=0.1)
radio2.pack(side="left",expand=True, anchor="center", pady=5)
# OPTATIVA 2
# Frame para la Optativa 2
frame_optativa2 = ctk.CTkFrame(frame_fase_voluntaria)
frame_optativa2.pack(pady=10, padx=10, fill="x")
ctk.CTkLabel(frame_optativa2, text="Optativa 2").pack(pady=(5,0))
entry6 = ctk.CTkEntry(frame_optativa2, placeholder_text="Nota optativa 2...")
entry6.pack(pady=5)
# Variable para almacenar la selección del RadioButton Ponderación 1
poneracion2 = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
# Frame para agrupar los botones de Optativa 1
frame_radio2 = ctk.CTkFrame(frame_optativa2)
frame_radio2.pack(pady=10, padx=10, fill="x")
# Etiqueta
ctk.CTkLabel(frame_radio2, text="Ponderación:").pack(pady=5)
# RadioButtons
radio3 = ctk.CTkRadioButton(frame_radio2, text=" 0.2", variable=poneracion2, value=0.2)
radio3.pack(side="left",pady=5,expand=True, anchor="e")
radio4 = ctk.CTkRadioButton(frame_radio2, text=" 0.1", variable=poneracion2, value=0.1)
radio4.pack(side="left",pady=5, expand=True, anchor="center")

# Función para obtener todas las notas
def obtener_notas():
    notas = [entry1.get()] + [entry.get() for entry in entries]
    print("Notas ingresadas:", notas)

# Botón para leer las notas
#boton = ctk.CTkButton(ventana_principal, text="Obtener Notas", command=obtener_notas)
#boton.pack(pady=20)

# Ejecutar la aplicación
ventana_principal.mainloop()
