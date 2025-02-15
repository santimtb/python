import subprocess
import customtkinter as ctk
from tkinter import messagebox
import json

# Función para validar mientras se escribe la nota de Bachiller
def valida_nota_bachiller(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        value = float(value_if_allowed)
        return 5 <= value <= 10 or value_if_allowed in ["1"]
    except ValueError:
        return False
    
# Función para validar mientras se escribe las notas de las asignaturas de la EBAU
def valida_nota(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        value = float(value_if_allowed)
        return 0 <= value <= 10
    except ValueError:
        return False

# Función cuando cualquier Entry obtiene el foco
#def on_focus_in(entry):
    #entry.configure(fg_color="lightgreen")  # Cambia el borde del Entry que recibe el foco

# Función cuando cualquier Entry pierde el foco
#def on_focus_out(entry):
    #entry.configure(fg_color="white")  # Restaura el border del Entry que pierde el foco

def valida_notas():
    bachi=entry_bachiller.get()
    # Nota Media de Bachillerato vacía
    if bachi == "" or bachi == "1":
        messagebox.showerror("Error", "La nota media de Bachillerato no puede estar vacía ni ser menor de 5.")
        entry_bachiller.focus()
        return False
    else:
        # Notas de la fase general vacías
        alguno_vacio = False
        for entry in entries:
            if entry.get() == "":
                entry.insert(0, "0")
                alguno_vacio = True

        # Notas de la fase específica vacías
        if entry_optativa1.get() == "":
            entry_optativa1.insert(0, "0")
            alguno_vacio = True
        if entry_optativa2.get() == "":
            entry_optativa2.insert(0, "0")
            alguno_vacio = True 

        if alguno_vacio:
            messagebox.showwarning("Advertencia", "Algunas notas están vacías y se han establecido a 0.")
        return True

def mostrar_resultados(resultados):
    # Crear una nueva ventana para mostrar los resultados
    ventana_resultados = ctk.CTkToplevel(ventana_principal)
    ventana_resultados.title("Resultados EBAU")
    ventana_resultados.geometry("600x540")

    # Mostrar los resultados en la nueva ventana
    
    # Resultado de la EBAU
    frame_resultado_ebau=ctk.CTkFrame(ventana_resultados)
    frame_resultado_ebau.pack(pady=10, padx=10, fill="x")
    frame_resultado_centrado=ctk.CTkFrame(frame_resultado_ebau, fg_color="green" if resultados[0][1] == "APTO" else "red")  
    frame_resultado_centrado.pack(pady=10)
    ctk.CTkLabel(frame_resultado_centrado, text="Resultado EBAU:", font=("Arial", 16, "bold")).pack(side="left", pady=10, padx=(20,10))
    ctk.CTkLabel(frame_resultado_centrado, text="  "+resultados[0][1]+"  ", font=("Arial", 16, "bold")).pack(side="left", pady=10,padx=(10,20))
    frame_resultado_centrado.pack(anchor="center")
    
    # Frame NAU
    frame_nau=ctk.CTkFrame(ventana_resultados)
    frame_nau.pack(pady=(0,5), padx=10, fill="x")
    frame_bachiller=ctk.CTkFrame(frame_nau, fg_color="transparent")  
    frame_bachiller.pack(pady=5)
    ctk.CTkLabel(frame_bachiller, text=resultados[1][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=20)   
    ctk.CTkLabel(frame_bachiller, text="  "+resultados[1][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5)   
    frame_nau.pack(anchor="center")
    frame_fase_general=ctk.CTkFrame(frame_nau, fg_color="transparent")
    frame_fase_general.pack(pady=5)
    ctk.CTkLabel(frame_fase_general, text=resultados[2][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=20) 
    ctk.CTkLabel(frame_fase_general, text="  "+resultados[2][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5)
    frame_fase_general.pack(anchor="center")
    frame_nau_centrado=ctk.CTkFrame(frame_nau, fg_color="#46705E")
    frame_nau_centrado.pack(pady=5, padx=10)
    ctk.CTkLabel(frame_nau_centrado, text=resultados[3][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=(20,10))  
    ctk.CTkLabel(frame_nau_centrado, text="  "+resultados[3][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5,padx=(10,20))
    frame_nau_centrado.pack(anchor="center")
    
    # Frame Ponderaciones
    frame_ponderaciones=ctk.CTkFrame(ventana_resultados)
    frame_ponderaciones.pack(pady=5, padx=10, fill="x")
    for asignatura, (nota, ponderacion, ponderada) in resultados[4][1]:
        frame=ctk.CTkFrame(frame_ponderaciones, fg_color="transparent")
        frame.pack(pady=5)
        ctk.CTkLabel(frame, text=f"{asignatura}:", font=("Arial", 14, "bold")).pack(side="left", pady=2, padx=20)   
        ctk.CTkLabel(frame, text="  "+nota+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=2)   
        ctk.CTkLabel(frame, text=f" x ({ponderacion})  ", font=("Arial", 14, "bold")).pack(side="left", pady=2)   
        ctk.CTkLabel(frame, text=" = "+ponderada+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=2)   
        frame.pack(anchor="center")
    frame_suma_ponderadas=ctk.CTkFrame(frame_ponderaciones, fg_color="#362C61")
    frame_suma_ponderadas.pack(pady=(5,10))
    ctk.CTkLabel(frame_suma_ponderadas, text=resultados[5][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=(20,10))   
    ctk.CTkLabel(frame_suma_ponderadas, text="  "+resultados[5][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5,padx=(10,20))
    frame_nat=ctk.CTkFrame(ventana_resultados, fg_color="transparent")
    frame_nat.pack(pady=5, padx=10, fill="x")
    frame_nat_centrado=ctk.CTkFrame(frame_nat, fg_color="#5E180B")
    ctk.CTkLabel(frame_nat_centrado, text=resultados[6][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=(20,10))
    ctk.CTkLabel(frame_nat_centrado, text="  "+resultados[6][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5,padx=(10,20))
    frame_nat_centrado.pack(anchor="center")
    
    # Añadir un botón para cerrar la ventana
    ctk.CTkButton(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy,fg_color="#BE0665", hover_color="#850447").pack(pady=20,side="right", padx=10)

    # Hacer que la ventana sea modal después de que se haya mostrado
    ventana_resultados.after(100, ventana_resultados.grab_set)
    
def resultado_ebau():
    if valida_notas():
        media_bachillerato = float(entry_bachiller.get())
        notas = obtener_notas_fase_general()
        #print("Nota Media de Bachillerato:", media_bachillerato)
        #print("Notas Fase General:", notas)
        #print("Ponderación Troncal de Modalidad:", ponderacion_troncal.get()) 
        notas_especifica = []
        notas_especifica.append((entry_optativa1.get(), ponderacion1.get()))
        notas_especifica.append((entry_optativa2.get(), ponderacion2.get()))
        #print("Notas Fase Específica:", notas_especifica)
        media_fase_general = sum([float(nota) for nota in notas]) / len(notas)
        print("Media Fase General:", media_fase_general)
        nau=media_bachillerato*0.6+media_fase_general*0.4
        #print("Nota de Acceso a la Universidad:", nau)
        ponderaciones = []
        ponderadas = []
        if float(notas[-1]) >= 5:
            ponderadas.append(float(notas[-1]) * ponderacion_troncal.get())
            ponderaciones.append(("Troncal", (notas[-1], ponderacion_troncal.get() , f"{float(notas[-1])*ponderacion_troncal.get():.3f}")))
        if float(entry_optativa1.get()) >= 5:
            ponderadas.append(float(entry_optativa1.get()) * ponderacion1.get())
            ponderaciones.append(("Optativa1", (entry_optativa1.get(), ponderacion1.get(),f"{float(entry_optativa1.get())*ponderacion1.get():.3f}")))
        if float(entry_optativa2.get()) >= 5:
            ponderadas.append(float(entry_optativa2.get()) * ponderacion2.get())
            ponderaciones.append(("Optativa2", (entry_optativa2.get(), ponderacion2.get(), f"{float(entry_optativa2.get())*ponderacion2.get():.3f}")))
        ponderadas = sorted(ponderadas, reverse=True)
        nat=nau+sum(ponderadas[:2])
        # Preparamos los resultados para su visualización
        # EBAU - APTO / NO APTO
        if media_fase_general >= 4 and nau >= 5:
            resultado_ebau = "APTO"
        else:
            resultado_ebau = "NO APTO"
        resultado = []
        resultado.append(("Resultado EBAU", resultado_ebau))
        resultado.append(("Nota Media de Bachillerato", f"{media_bachillerato:.2f}"))
        resultado.append(("Media Fase General", f"{media_fase_general:.2f}"))
        resultado.append(("NAU", f"{nau:.2f}"))
        resultado.append(("Ponderaciones", ponderaciones))
        resultado.append(("Suma ponderadas", f"{sum(ponderadas[:2]):.3f}"))
        resultado.append(("NAT", f"{nat:.3f}"))
        # Mostrar los resultados en una nueva ventana
        #print(ponderaciones)
        mostrar_resultados(resultado)
    
    
# Función para obtener todas las notas
def obtener_notas_fase_general():
    notas = [entry.get() for entry in entries]
    #print("Notas ingresadas:", notas)
    return notas

def abre_notas_corte():
    subprocess.Popen(["python3", "notas_corte2.py"])
    
def abre_ponderaciones():
    subprocess.Popen(["python3", "pondera.py"])
        
# Configurar apariencia y tema
ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # Tema de colores

# Crear la ventana principal
ventana_principal = ctk.CTk()
ventana_principal.geometry("800x740+200+200")
ventana_principal.title("Simulador EBAU")

# Registramos la función para validar mientras se escribe en un Entry
valida_nota_bachiller_cmd = ventana_principal.register(valida_nota_bachiller)
valida_nota_cmd = ventana_principal.register(valida_nota)

# Frame para la Nota Media de Bachillerato
frame_bachiller = ctk.CTkFrame(ventana_principal)
frame_bachiller.pack(pady=(10,5), padx=10, fill="x")

ctk.CTkLabel(frame_bachiller, text="Nota Media de Bachillerato:", font=("Arial", 14, "bold")).pack(pady=(5,0))
entry_bachiller = ctk.CTkEntry(frame_bachiller, validate="key", validatecommand=(valida_nota_bachiller_cmd, '%P'), placeholder_text="Nota media de bachiller...", justify="center",width=250)
#entry1.bind("<FocusIn>", lambda e: on_focus_in(entry1))   # Evento cuando obtiene el foco
#entry1.bind("<FocusOut>", lambda e: on_focus_out(entry1)) # Evento cuando pierde el foco
entry_bachiller.pack(pady=10)

# Frame central
frame_central = ctk.CTkFrame(ventana_principal)
frame_central.pack(pady=(5,5), padx=10, fill="x")

# Frame para la Fase Obligatoria
frame_fase_obligatoria = ctk.CTkFrame(frame_central, width=400)
frame_fase_obligatoria.pack(side="left", pady=(10,10), padx=(10,5), fill="both", expand=True)

titulo = ctk.CTkLabel(frame_fase_obligatoria, text="Fase Obligatoria", font=("Arial", 14, "bold"), anchor="center")
titulo.pack(fill="x", padx=10, pady=(5, 0))  

fase_general = ("Castellano: lengua y literatura", "Valenciano: lengua i literaura", "Lengua Extranjera", "Historia de España/Filosofía","Troncal de modalidad")

entries = []  # Lista para almacenar los entry de la Fase General
for i in range(4):  # Asignaturas de la Fase General excepto la troncal de modalidad que lleva ponderación
    ctk.CTkLabel(frame_fase_obligatoria, text=f"{fase_general[i]}:").pack(pady=(5,0))
    entry = ctk.CTkEntry(frame_fase_obligatoria, validate="key", validatecommand=(valida_nota_cmd, '%P'), width=250, placeholder_text=f"Nota {fase_general[i]}", justify="center")
    entry.pack(pady=(0,5))
    entries.append(entry)

# Falta la troncal de modalidad (Matemáticas)
# TRONCAL DE MODALIDAD
# Frame para la TRONCAL DE MODALIDAD
frame_troncal = ctk.CTkFrame(frame_fase_obligatoria)
frame_troncal.pack(pady=(5,5), padx=10, fill="x", expand=True)
ctk.CTkLabel(frame_troncal, text=f"{fase_general[-1]}").pack(pady=(5,0))
entry = ctk.CTkEntry(frame_troncal, validate="key", validatecommand=(valida_nota_cmd, '%P'), width=250, placeholder_text=f"Nota {fase_general[-1]}...", justify="center")
entry.pack(pady=5)
entries.append(entry)
# Variable para almacenar la selección del RadioButton Ponderación troncal
ponderacion_troncal = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
# Frame para agrupar los botones de ponderación troncal
frame_pondera_troncal = ctk.CTkFrame(frame_troncal)
frame_pondera_troncal.pack(pady=10, padx=10, fill="x")
# Etiqueta
ctk.CTkLabel(frame_pondera_troncal, text="Ponderación:").pack(pady=5)
# RadioButtons
radio_troncal1 = ctk.CTkRadioButton(frame_pondera_troncal, text=" 0.2", variable=ponderacion_troncal, value=0.2)
radio_troncal1.pack(side="left",expand=True, anchor="e",pady=(0,10))    
radio_troncal2 = ctk.CTkRadioButton(frame_pondera_troncal, text=" 0.1", variable=ponderacion_troncal, value=0.1)
radio_troncal2.pack(side="left",expand=True, anchor="center", pady=(0,10))

# Frame para la Fase Voluntaria
frame_fase_voluntaria = ctk.CTkFrame(frame_central, width=400)
frame_fase_voluntaria.pack(side="left", pady=(10,10), padx=(5,10), fill="both", expand=True)
titulo2 = ctk.CTkLabel(frame_fase_voluntaria, text="Fase Voluntaria", font=("Arial", 14, "bold"), anchor="center")
titulo2.pack(fill="x", padx=10, pady=(5, 0))  
#OPTATIVA 1
# Frame para la Optativa 1
frame_optativa1 = ctk.CTkFrame(frame_fase_voluntaria)
frame_optativa1.pack(pady=(5,5), padx=10, fill="x", expand=True)
ctk.CTkLabel(frame_optativa1, text="Optativa 1").pack(pady=(5,0))
entry_optativa1 = ctk.CTkEntry(frame_optativa1, validate="key", validatecommand=(valida_nota_cmd, '%P'), placeholder_text="Nota optativa 1...", justify="center")
entry_optativa1.pack(pady=5)
# Variable para almacenar la selección del RadioButton Ponderación 1
ponderacion1 = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
# Frame para agrupar los botones de Optativa 1
frame_radio1 = ctk.CTkFrame(frame_optativa1)
frame_radio1.pack(pady=10, padx=10, fill="x")
# Etiqueta
ctk.CTkLabel(frame_radio1, text="Ponderación:").pack(pady=5)
# RadioButtons
radio1 = ctk.CTkRadioButton(frame_radio1, text=" 0.2", variable=ponderacion1, value=0.2)
radio1.pack(side="left",expand=True, anchor="e",pady=(0,10))    
radio2 = ctk.CTkRadioButton(frame_radio1, text=" 0.1", variable=ponderacion1, value=0.1)
radio2.pack(side="left",expand=True, anchor="center", pady=(0,10))
# OPTATIVA 2
# Frame para la Optativa 2
frame_optativa2 = ctk.CTkFrame(frame_fase_voluntaria)
frame_optativa2.pack(pady=(5,10), padx=10, fill="x")
ctk.CTkLabel(frame_optativa2, text="Optativa 2").pack(pady=(5,0))
entry_optativa2 = ctk.CTkEntry(frame_optativa2, validate="key", validatecommand=(valida_nota_cmd, '%P'), placeholder_text="Nota optativa 2...", justify="center")
entry_optativa2.pack(pady=5)
# Variable para almacenar la selección del RadioButton Ponderación 1
ponderacion2 = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
# Frame para agrupar los botones de Optativa 1
frame_radio2 = ctk.CTkFrame(frame_optativa2)
frame_radio2.pack(pady=10, padx=10, fill="x")
# Etiqueta
ctk.CTkLabel(frame_radio2, text="Ponderación:").pack(pady=5)
# RadioButtons
radio3 = ctk.CTkRadioButton(frame_radio2, text=" 0.2", variable=ponderacion2, value=0.2)
radio3.pack(side="left",pady=(0,10),expand=True, anchor="e")
radio4 = ctk.CTkRadioButton(frame_radio2, text=" 0.1", variable=ponderacion2, value=0.1)
radio4.pack(side="left",pady=(0,10), expand=True, anchor="center")


# Frame para el botón de Calcular
frame_boton = ctk.CTkFrame(ventana_principal)
frame_boton.pack(pady=(5,5), padx=10, fill="x")
# Botón para leer las notas
boton = ctk.CTkButton(frame_boton, text="Obtener resultado EBAU", command=resultado_ebau)
boton.pack(pady=10)

# Frame para los botones adicionales para Consultar las Notas de Corte y Ponderaciones
frame_botones = ctk.CTkFrame(ventana_principal)
frame_botones.pack(pady=(5,5), padx=10, fill="x")
#frame_botones_centro
frame_botones_centro = ctk.CTkFrame(frame_botones,fg_color="transparent")
frame_botones_centro.pack(pady=(5,5), padx=10)
# Botón para Notas de Corte
boton_notas_corte = ctk.CTkButton(frame_botones_centro, text="Notas de Corte 2024", command=abre_notas_corte,fg_color="#B1B11D", hover_color="#5C5C2E")
boton_notas_corte.pack(side="left",pady=10,padx=10)
# Botón para Ponderaciones
boton_ponderaciones = ctk.CTkButton(frame_botones_centro, text="Ponderaciones 2024", command=abre_ponderaciones,fg_color="#1DB1AC", hover_color="#2E5C5A")
boton_ponderaciones.pack(side="left",pady=10,padx=10)
frame_botones_centro.pack(anchor="center")
# Ejecutar la aplicación
ventana_principal.mainloop()
