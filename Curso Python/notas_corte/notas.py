import subprocess
import customtkinter as ctk
from tkinter import messagebox
import json

# Configurar apariencia y tema
ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # Tema de colores

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        # Crear la ventana principal
        self.root.geometry("800x810+200+200")
        self.root.title("Simulador EBAU 2025")
        # Registramos la función para validar mientras se escribe en un Entry
        self.valida_nota_bachiller_cmd = root.register(self.valida_nota_bachiller)
        self.valida_nota_cmd = root.register(self.valida_nota)
        
        # Frame para el título de la ventana
        self.frame_titulo = ctk.CTkFrame(root,fg_color="#1DB1AC")
        self.frame_titulo.pack(padx=10,pady=10,fill="x",expand="True")
        self.label_titulo = ctk.CTkLabel(self.frame_titulo, text ="Simulador de Notas de la EBAU 2025",font=("Verdana",20,"bold"))
        self.label_titulo.pack(pady=10)
        # Frame para la Nota Media de Bachillerato
        self.frame_bachiller = ctk.CTkFrame(root)
        self.frame_bachiller.pack(pady=(10,5), padx=10, fill="x")

        ctk.CTkLabel(self.frame_bachiller, text="Nota Media de Bachillerato:", font=("Arial", 14, "bold")).pack(pady=(5,0))
        self.entry_bachiller = ctk.CTkEntry(self.frame_bachiller, validate="key", validatecommand=(self.valida_nota_bachiller_cmd, '%P'), placeholder_text="Nota media de bachiller...", justify="center",width=250)
        #entry1.bind("<FocusIn>", lambda e: on_focus_in(entry1))   # Evento cuando obtiene el foco
        #entry1.bind("<FocusOut>", lambda e: on_focus_out(entry1)) # Evento cuando pierde el foco
        self.entry_bachiller.pack(pady=10)

        # Frame central
        self.frame_central = ctk.CTkFrame(root)
        self.frame_central.pack(pady=(5,5), padx=10, fill="x")

        # Frame para la Fase Obligatoria
        self.frame_fase_obligatoria = ctk.CTkFrame(self.frame_central, width=400)
        self.frame_fase_obligatoria.pack(side="left", pady=(10,10), padx=(10,5), fill="both", expand=True)

        self.titulo = ctk.CTkLabel(self.frame_fase_obligatoria, text="Fase Obligatoria", font=("Arial", 14, "bold"), anchor="center")
        self.titulo.pack(fill="x", padx=10, pady=(5, 0))  

        self.fase_general = ("Castellano: lengua y literatura", "Valenciano: lengua i literaura", "Lengua Extranjera", "Historia de España/Filosofía","Troncal de modalidad")

        self.entries = []  # Lista para almacenar los entry de la Fase General
        for i in range(4):  # Asignaturas de la Fase General excepto la troncal de modalidad que lleva ponderación
            ctk.CTkLabel(self.frame_fase_obligatoria, text=f"{self.fase_general[i]}:").pack(pady=(5,0))
            self.entry = ctk.CTkEntry(self.frame_fase_obligatoria, validate="key", validatecommand=(self.valida_nota_cmd, '%P'), width=250, placeholder_text=f"Nota {self.fase_general[i]}", justify="center")
            self.entry.pack(pady=(0,5))
            self.entries.append(self.entry)

        # Falta la troncal de modalidad (Matemáticas)
        # TRONCAL DE MODALIDAD
        # Frame para la TRONCAL DE MODALIDAD
        self.frame_troncal = ctk.CTkFrame(self.frame_fase_obligatoria)
        self.frame_troncal.pack(pady=(5,5), padx=10, fill="x", expand=True)
        ctk.CTkLabel(self.frame_troncal, text=f"{self.fase_general[-1]}").pack(pady=(5,0))
        self.entry = ctk.CTkEntry(self.frame_troncal, validate="key", validatecommand=(self.valida_nota_cmd, '%P'), width=250, placeholder_text=f"Nota {self.fase_general[-1]}...", justify="center")
        self.entry.pack(pady=5)
        self.entries.append(self.entry)
        # Variable para almacenar la selección del RadioButton Ponderación troncal
        self.ponderacion_troncal = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
        # Frame para agrupar los botones de ponderación troncal
        self.frame_pondera_troncal = ctk.CTkFrame(self.frame_troncal)
        self.frame_pondera_troncal.pack(pady=10, padx=10, fill="x")
        # Etiqueta
        ctk.CTkLabel(self.frame_pondera_troncal, text="Ponderación:").pack(pady=5)
        # RadioButtons
        self.radio_troncal1 = ctk.CTkRadioButton(self.frame_pondera_troncal, text=" 0.2", variable=self.ponderacion_troncal, value=0.2)
        self.radio_troncal1.pack(side="left",expand=True, anchor="e",pady=(0,10))    
        self.radio_troncal2 = ctk.CTkRadioButton(self.frame_pondera_troncal, text=" 0.1", variable=self.ponderacion_troncal, value=0.1)
        self.radio_troncal2.pack(side="left",expand=True, anchor="center", pady=(0,10))

        # Frame para la Fase Voluntaria
        self.frame_fase_voluntaria = ctk.CTkFrame(self.frame_central, width=400)
        self.frame_fase_voluntaria.pack(side="left", pady=(10,10), padx=(5,10), fill="both", expand=True)
        self.titulo2 = ctk.CTkLabel(self.frame_fase_voluntaria, text="Fase Voluntaria", font=("Arial", 14, "bold"), anchor="center")
        self.titulo2.pack(fill="x", padx=10, pady=(5, 0))  
        #OPTATIVA 1
        # Frame para la Optativa 1
        self.frame_optativa1 = ctk.CTkFrame(self.frame_fase_voluntaria)
        self.frame_optativa1.pack(pady=(5,5), padx=10, fill="x", expand=True)
        ctk.CTkLabel(self.frame_optativa1, text="Optativa 1").pack(pady=(5,0))
        self.entry_optativa1 = ctk.CTkEntry(self.frame_optativa1, validate="key", validatecommand=(self.valida_nota_cmd, '%P'), placeholder_text="Nota optativa 1...", justify="center")
        self.entry_optativa1.pack(pady=5)
        # Variable para almacenar la selección del RadioButton Ponderación 1
        self.ponderacion1 = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
        # Frame para agrupar los botones de Optativa 1
        self.frame_radio1 = ctk.CTkFrame(self.frame_optativa1)
        self.frame_radio1.pack(pady=10, padx=10, fill="x")
        # Etiqueta
        ctk.CTkLabel(self.frame_radio1, text="Ponderación:").pack(pady=5)
        # RadioButtons
        self.radio1 = ctk.CTkRadioButton(self.frame_radio1, text=" 0.2", variable=self.ponderacion1, value=0.2)
        self.radio1.pack(side="left",expand=True, anchor="e",pady=(0,10))    
        self.radio2 = ctk.CTkRadioButton(self.frame_radio1, text=" 0.1", variable=self.ponderacion1, value=0.1)
        self.radio2.pack(side="left",expand=True, anchor="center", pady=(0,10))
        # OPTATIVA 2
        # Frame para la Optativa 2
        self.frame_optativa2 = ctk.CTkFrame(self.frame_fase_voluntaria)
        self.frame_optativa2.pack(pady=(5,10), padx=10, fill="x")
        ctk.CTkLabel(self.frame_optativa2, text="Optativa 2").pack(pady=(5,0))
        self.entry_optativa2 = ctk.CTkEntry(self.frame_optativa2, validate="key", validatecommand=(self.valida_nota_cmd, '%P'), placeholder_text="Nota optativa 2...", justify="center")
        self.entry_optativa2.pack(pady=5)
        # Variable para almacenar la selección del RadioButton Ponderación 1
        self.ponderacion2 = ctk.DoubleVar(value=0.2)  # Valor por defecto 0.2
        # Frame para agrupar los botones de Optativa 1
        self.frame_radio2 = ctk.CTkFrame(self.frame_optativa2)
        self.frame_radio2.pack(pady=10, padx=10, fill="x")
        # Etiqueta
        ctk.CTkLabel(self.frame_radio2, text="Ponderación:").pack(pady=5)
        # RadioButtons
        self.radio3 = ctk.CTkRadioButton(self.frame_radio2, text=" 0.2", variable=self.ponderacion2, value=0.2)
        self.radio3.pack(side="left",pady=(0,10),expand=True, anchor="e")
        self.radio4 = ctk.CTkRadioButton(self.frame_radio2, text=" 0.1", variable=self.ponderacion2, value=0.1)
        self.radio4.pack(side="left",pady=(0,10), expand=True, anchor="center")


        # Frame para el botón de Calcular
        self.frame_boton = ctk.CTkFrame(root)
        self.frame_boton.pack(pady=(5,5), padx=10, fill="x")
        # Botón para leer las notas
        self.boton = ctk.CTkButton(self.frame_boton, text="Obtener resultado EBAU", command=self.resultado_ebau)
        self.boton.pack(pady=10)

        # Frame para los botones adicionales para Consultar las Notas de Corte y Ponderaciones
        self.frame_botones = ctk.CTkFrame(root)
        self.frame_botones.pack(pady=(5,5), padx=10, fill="x")
        #frame_botones_centro
        self.frame_botones_centro = ctk.CTkFrame(self.frame_botones,fg_color="transparent")
        self.frame_botones_centro.pack(pady=(5,5), padx=10)
        # Botón para Notas de Corte
        self.boton_notas_corte = ctk.CTkButton(self.frame_botones_centro, text="Notas de Corte 2024", command=self.abre_notas_corte,fg_color="#B1B11D", hover_color="#5C5C2E")
        self.boton_notas_corte.pack(side="left",pady=10,padx=10)
        # Botón para Ponderaciones
        self.boton_ponderaciones = ctk.CTkButton(self.frame_botones_centro, text="Ponderaciones 2024", command=self.abre_ponderaciones,fg_color="#1DB1AC", hover_color="#2E5C5A")
        self.boton_ponderaciones.pack(side="left",pady=10,padx=10)
        self.boton_salir = ctk.CTkButton(self.frame_botones_centro, text = "Salir", command=root.destroy,fg_color="#C1194E", hover_color="#6A0E2B")
        self.boton_salir.pack(side="right",padx=10,pady=10)
        self.frame_botones_centro.pack()
        
    # Función para validar mientras se escribe la nota de Bachiller
    def valida_nota_bachiller(self,value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            value = float(value_if_allowed)
            return 5 <= value <= 10 or value_if_allowed in ["1"]
        except ValueError:
            return False
    
    # Función para validar mientras se escribe las notas de las asignaturas de la EBAU
    def valida_nota(self,value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            value = float(value_if_allowed)
            return 0 <= value <= 10
        except ValueError:
            return False

    def valida_notas(self):
        bachi=self.entry_bachiller.get()
        # Nota Media de Bachillerato vacía
        if bachi == "" or bachi == "1":
            messagebox.showerror("Error", "La nota media de Bachillerato no puede estar vacía ni ser menor de 5.")
            self.entry_bachiller.focus()
            return False
        else:
            # Notas de la fase general vacías
            alguno_vacio = False
            for entry in self.entries:
                if entry.get() == "":
                    entry.insert(0, "0")
                    alguno_vacio = True

            # Notas de la fase específica vacías
            if self.entry_optativa1.get() == "":
                self.entry_optativa1.insert(0, "0")
                alguno_vacio = True
            if self.entry_optativa2.get() == "":
                self.entry_optativa2.insert(0, "0")
                alguno_vacio = True 

            if alguno_vacio:
                messagebox.showwarning("Advertencia", "Algunas notas están vacías y se han establecido a 0.")
            return True

    def mostrar_resultados(self,resultados):
        # Crear una nueva ventana para mostrar los resultados
        self.ventana_resultados = ctk.CTkToplevel(self.root)
        self.ventana_resultados.title("Resultados EBAU")
        self.ventana_resultados.geometry("600x540")

        # Mostrar los resultados en la nueva ventana
        
        # Resultado de la EBAU
        self.ventana_resultados.frame_resultado_ebau=ctk.CTkFrame(self.ventana_resultados)
        self.ventana_resultados.frame_resultado_ebau.pack(pady=10, padx=10, fill="x")
        self.ventana_resultados.frame_resultado_centrado=ctk.CTkFrame(self.ventana_resultados.frame_resultado_ebau, fg_color="green" if resultados[0][1] == "APTO" else "red")  
        self.ventana_resultados.frame_resultado_centrado.pack(pady=10)
        ctk.CTkLabel(self.ventana_resultados.frame_resultado_centrado, text="Resultado EBAU:", font=("Arial", 16, "bold")).pack(side="left", pady=10, padx=(20,10))
        ctk.CTkLabel(self.ventana_resultados.frame_resultado_centrado, text="  "+resultados[0][1]+"  ", font=("Arial", 16, "bold")).pack(side="left", pady=10,padx=(10,20))
        self.ventana_resultados.frame_resultado_centrado.pack(anchor="center")
        
        # Frame NAU
        self.ventana_resultados.frame_nau=ctk.CTkFrame(self.ventana_resultados)
        self.ventana_resultados.frame_nau.pack(pady=(0,5), padx=10, fill="x")
        self.ventana_resultados.frame_bachiller=ctk.CTkFrame(self.ventana_resultados.frame_nau, fg_color="transparent")  
        self.ventana_resultados.frame_bachiller.pack(pady=5)
        ctk.CTkLabel(self.ventana_resultados.frame_bachiller, text=resultados[1][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=20)   
        ctk.CTkLabel(self.ventana_resultados.frame_bachiller, text="  "+resultados[1][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5)   
        self.ventana_resultados.frame_nau.pack(anchor="center")
        self.ventana_resultados.frame_fase_general=ctk.CTkFrame(self.ventana_resultados.frame_nau, fg_color="transparent")
        self.ventana_resultados.frame_fase_general.pack(pady=5)
        ctk.CTkLabel(self.ventana_resultados.frame_fase_general, text=resultados[2][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=20) 
        ctk.CTkLabel(self.ventana_resultados.frame_fase_general, text="  "+resultados[2][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5)
        self.ventana_resultados.frame_fase_general.pack(anchor="center")
        self.ventana_resultados.frame_nau_centrado=ctk.CTkFrame(self.ventana_resultados.frame_nau, fg_color="#46705E")
        self.ventana_resultados.frame_nau_centrado.pack(pady=5, padx=10)
        ctk.CTkLabel(self.ventana_resultados.frame_nau_centrado, text=resultados[3][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=(20,10))  
        ctk.CTkLabel(self.ventana_resultados.frame_nau_centrado, text="  "+resultados[3][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5,padx=(10,20))
        self.ventana_resultados.frame_nau_centrado.pack(anchor="center")
        
        # Frame Ponderaciones
        self.ventana_resultados.frame_ponderaciones=ctk.CTkFrame(self.ventana_resultados)
        self.ventana_resultados.frame_ponderaciones.pack(pady=5, padx=10, fill="x")
        for asignatura, (nota, ponderacion, ponderada) in resultados[4][1]:
            self.ventana_resultados.frame=ctk.CTkFrame(self.ventana_resultados.frame_ponderaciones, fg_color="transparent")
            self.ventana_resultados.frame.pack(pady=5)
            ctk.CTkLabel(self.ventana_resultados.frame, text=f"{asignatura}:", font=("Arial", 14, "bold")).pack(side="left", pady=2, padx=20)   
            ctk.CTkLabel(self.ventana_resultados.frame, text="  "+nota+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=2)   
            ctk.CTkLabel(self.ventana_resultados.frame, text=f" x ({ponderacion})  ", font=("Arial", 14, "bold")).pack(side="left", pady=2)   
            ctk.CTkLabel(self.ventana_resultados.frame, text=" = "+ponderada+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=2)   
            self.ventana_resultados.frame.pack(anchor="center")
        self.ventana_resultados.frame_suma_ponderadas=ctk.CTkFrame(self.ventana_resultados.frame_ponderaciones, fg_color="#362C61")
        self.ventana_resultados.frame_suma_ponderadas.pack(pady=(5,10))
        ctk.CTkLabel(self.ventana_resultados.frame_suma_ponderadas, text=resultados[5][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=(20,10))   
        ctk.CTkLabel(self.ventana_resultados.frame_suma_ponderadas, text="  "+resultados[5][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5,padx=(10,20))
        self.ventana_resultados.frame_nat=ctk.CTkFrame(self.ventana_resultados, fg_color="transparent")
        self.ventana_resultados.frame_nat.pack(pady=5, padx=10, fill="x")
        self.ventana_resultados.frame_nat_centrado=ctk.CTkFrame(self.ventana_resultados.frame_nat, fg_color="#5E180B")
        ctk.CTkLabel(self.ventana_resultados.frame_nat_centrado, text=resultados[6][0], font=("Arial", 14, "bold")).pack(side="left", pady=5, padx=(20,10))
        ctk.CTkLabel(self.ventana_resultados.frame_nat_centrado, text="  "+resultados[6][1]+"  ", font=("Arial", 14, "bold")).pack(side="left", pady=5,padx=(10,20))
        self.ventana_resultados.frame_nat_centrado.pack(anchor="center")
        
        # Añadir un botón para cerrar la ventana
        ctk.CTkButton(self.ventana_resultados, text="Cerrar", command=self.ventana_resultados.destroy,fg_color="#BE0665", hover_color="#850447").pack(pady=20,side="right", padx=10)

        # Hacer que la ventana sea modal después de que se haya mostrado
        self.ventana_resultados.after(100, self.ventana_resultados.grab_set)
        
    def resultado_ebau(self):
        if self.valida_notas():
            media_bachillerato = float(self.entry_bachiller.get())
            notas = self.obtener_notas_fase_general()
            #print("Nota Media de Bachillerato:", media_bachillerato)
            #print("Notas Fase General:", notas)
            #print("Ponderación Troncal de Modalidad:", ponderacion_troncal.get()) 
            notas_especifica = []
            notas_especifica.append((self.entry_optativa1.get(), self.ponderacion1.get()))
            notas_especifica.append((self.entry_optativa2.get(), self.ponderacion2.get()))
            #print("Notas Fase Específica:", notas_especifica)
            media_fase_general = sum([float(nota) for nota in notas]) / len(notas)
            nau=media_bachillerato*0.6+media_fase_general*0.4
            #print("Nota de Acceso a la Universidad:", nau)
            ponderaciones = []
            ponderadas = []
            if float(notas[-1]) >= 5:
                ponderadas.append(float(notas[-1]) * self.ponderacion_troncal.get())
                ponderaciones.append(("Troncal", (notas[-1], self.ponderacion_troncal.get() , f"{float(notas[-1])*self.ponderacion_troncal.get():.3f}")))
            if float(self.entry_optativa1.get()) >= 5:
                ponderadas.append(float(self.entry_optativa1.get()) * self.ponderacion1.get())
                ponderaciones.append(("Optativa1", (self.entry_optativa1.get(), self.ponderacion1.get(),f"{float(self.entry_optativa1.get())*self.ponderacion1.get():.3f}")))
            if float(self.entry_optativa2.get()) >= 5:
                ponderadas.append(float(self.entry_optativa2.get()) * self.ponderacion2.get())
                ponderaciones.append(("Optativa2", (self.entry_optativa2.get(), self.ponderacion2.get(), f"{float(self.entry_optativa2.get())*self.ponderacion2.get():.3f}")))
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
            self.mostrar_resultados(resultado)
    
    # Función para obtener todas las notas
    def obtener_notas_fase_general(self):
        notas = [entry.get() for entry in self.entries]
        #print("Notas ingresadas:", notas)
        return notas

    def abre_notas_corte(self):
        subprocess.Popen(["python3", "notas_corte2.py"])
        
    def abre_ponderaciones(self):
        subprocess.Popen(["python3", "pondera.py"])
        
def main():
    root = ctk.CTk()
    app = SimuladorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()