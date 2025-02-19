import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntry
from PIL import Image, ImageTk
import json
import sys
import os

# Configurar apariencia y tema
ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # Tema de colores

class AutocompleteEntryWithPlaceholder(AutocompleteEntry):
    def __init__(self, master=None, placeholder="Buscar...", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self.bind('<FocusIn>', self._clear_placeholder)
        self.bind('<FocusOut>', self._add_placeholder)
        self.placeholder_active = True

    def _clear_placeholder(self, event=None):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.placeholder_active = False

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.placeholder_active = True
            
class CorteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Notas de Corte")
        self.root.geometry("800x700+100+100")
        self.icon = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'assets', 'applogo.ico'))
        self.root.iconphoto(False, self.icon)
        self.data_corte = self.leer_json()
        # Crear una lista de titulaciones, universidades y facultades para el autocompletado
        self.titulaciones = [item['Titulación'] for item in self.data_corte]
        self.universidades = list(set(item['Universidad'] for item in self.data_corte))
        self.facultades = list(set(item['Facultad'] for item in self.data_corte))

        # Frame para el título de la ventana
        self.frame_titulo = ctk.CTkFrame(root,fg_color="#1DB1AC")
        self.frame_titulo.pack(padx=10,pady=10,fill="x",expand="True")
        self.label_titulo = ctk.CTkLabel(self.frame_titulo, text="Notas de Corte de la Comunidad Valenciana 2024", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)
        
        # Entry con autocompletado y marcador de posición
        #Creamos un Frame contenedor
        self.frame_titulacion = ctk.CTkFrame(root)
        self.frame_titulacion.pack(fill="x",expand=True,padx=10,pady=10)
        # Frame para centrar los widgets
        self.frame_titulacion_widgets=ctk.CTkFrame(self.frame_titulacion,fg_color="transparent")
        self.frame_titulacion_widgets.pack()
        self.label_titulacion = ctk.CTkLabel(self.frame_titulacion_widgets, text="Titulación:", font=("Verdana",14,"bold"))
        self.label_titulacion.pack(side="left",padx=10,pady=10)
        self.entry_titulacion = AutocompleteEntryWithPlaceholder(self.frame_titulacion_widgets, completevalues=self.titulaciones, placeholder="Buscar Titulación", width=50)
        self.entry_titulacion.pack(side="left",padx=10,pady=10)
        self.frame_titulacion_widgets.pack(anchor="center")

        # Filtro por universidad y facultad
        # Creamos un Frame contenedor 
        self.frame_filtros = ctk.CTkFrame(root)
        self.frame_filtros.pack(fill="x",expand=True,padx=10,pady=5)
        # Frame para centrar los widgets
        self.frame_filtros_widgets=ctk.CTkFrame(self.frame_filtros)
        self.frame_filtros_widgets.pack()
        # Combobox para universidades
        self.combo_universidad = ttk.Combobox(self.frame_filtros_widgets, values=self.universidades)
        self.combo_universidad.pack(side="left",padx=10,pady=10)
        self.combo_universidad.set("Seleccionar Universidad")
        # Combobox para facultades
        self.combo_facultad = ttk.Combobox(self.frame_filtros_widgets, values=self.facultades)
        self.combo_facultad.pack(side="left", padx=10,pady=10)
        self.combo_facultad.set("Seleccionar Facultad")
        self.frame_filtros_widgets.pack(anchor="center")

        # Lista para mostrar resultados
        self.listbox = tk.Listbox(root, width=90)
        self.listbox.pack(pady=10)
        self.listbox.bind('<<ListboxSelect>>', self.show_details)

        # Diccionario para mapear índices de la Listbox a elementos de datos
        self.index_map = {}

        self.frame_nota_general = ctk.CTkFrame(root,fg_color="transparent")
        self.frame_nota_general.pack(fill="x",expand=True,padx=10,pady=5)
        self.frame_nota_general_centrado = ctk.CTkFrame(self.frame_nota_general,fg_color="transparent")
        self.frame_nota_general_centrado.pack()
        # Etiqueta para mostrar la nota de corte general
        self.label_general = ctk.CTkLabel(self.frame_nota_general_centrado, text="", font=("Arial",18,"bold"), text_color="#62BC63")
        self.label_general.pack(padx=20,pady=5)
        self.frame_nota_general_centrado.pack(anchor="center")
        # Checkbutton para mostrar la nota de deportista de élite
        self.show_deportista_var = tk.BooleanVar()
        self.check_deportista = ctk.CTkCheckBox(root, text="Mostrar Nota Deportista", variable=self.show_deportista_var, command=self.update_details, font=("Arial",14,"bold"))
        self.check_deportista.pack(pady=5)


        # Etiqueta para mostrar la nota de deportista de élite
        self.label_deportista = ctk.CTkLabel(root, text="", font=("Arial",16,"bold"),text_color="#FC429A",fg_color="transparent")
        self.label_deportista.pack(padx=20,pady=10)

        self.frame_botones = ctk.CTkFrame(root, fg_color="transparent")
        self.frame_botones.pack(padx=10,pady=10)
        self.frame_botones_centrados = ctk.CTkFrame(self.frame_botones, fg_color="transparent")
        self.frame_botones_centrados.pack(padx=20,pady=10)
        
        # Botón para resetear filtros
        self.reset_button = ctk.CTkButton(self.frame_botones_centrados, text="Resetear Filtros", command=self.reset_filters,fg_color="#A88E28", hover_color="#5C5C2E")
        self.reset_button.pack(padx=20,pady=5,side="left")

        # Botón para cerrar la aplicación
        self.close_button = ctk.CTkButton(self.frame_botones_centrados, text="Cerrar", command=self.root.destroy, fg_color="#6F4257", hover_color="#533141")
        self.close_button.pack(padx=20,pady=5,side="left")

        self.frame_botones_centrados.pack(anchor="center")
        # Vincular eventos
        self.entry_titulacion.bind('<KeyRelease>', self.apply_filters)
        self.combo_universidad.bind('<<ComboboxSelected>>', self.apply_filters)
        self.combo_facultad.bind('<<ComboboxSelected>>', self.apply_filters)

    def leer_json(self):
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, 'assets', 'titulaciones.json')
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    
    def apply_filters(self, event=None):
        search_term = self.entry_titulacion.get().lower()
        if self.entry_titulacion.placeholder_active:
            search_term = ""
        selected_universidad = self.combo_universidad.get()
        selected_facultad = self.combo_facultad.get()

        self.listbox.delete(0, tk.END)
        self.index_map.clear()
        for index, item in enumerate(self.data_corte):
            if (search_term in item['Titulación'].lower() and
                (selected_universidad == "Seleccionar Universidad" or item['Universidad'] == selected_universidad) and
                (selected_facultad == "Seleccionar Facultad" or item['Facultad'] == selected_facultad)):
                listbox_index = self.listbox.size()
                self.listbox.insert(tk.END, f"{item['Titulación']} - {item['Facultad']}")
                self.index_map[listbox_index] = index

    def show_details(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            listbox_index = selected_index[0]
            data_index = self.index_map[listbox_index]
            item = self.data_corte[data_index]
            self.label_general.configure(text=f"Nota de corte General: {item['General']}")
            self.selected_item = item
            self.update_details()

    def update_details(self):
        if hasattr(self, 'selected_item'):
            if self.show_deportista_var.get():
                self.label_deportista.configure(text=f"Nota de corte Deportista de élite: {self.selected_item['Deportista']}")
            else:
                self.label_deportista.configure(text="")

    def reset_filters(self):
        self.entry_titulacion.delete(0, tk.END)
        self.entry_titulacion.insert(0, self.entry_titulacion.placeholder)
        self.combo_universidad.set("Seleccionar Universidad")
        self.combo_facultad.set("Seleccionar Facultad")
        self.listbox.delete(0, tk.END)
        self.label_general.configure(text="")
        self.label_deportista.configure(text="")
        self.show_deportista_var.set(False)

class PonderacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabla de Ponderaciones")
        self.root.geometry("800x600+100+100")
        self.icon = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'assets', 'applogo.ico'))
        self.root.iconphoto(False, self.icon)
        self.data_ponderaciones = self.leer_json()
        self.frame_filtros = ctk.CTkFrame(root)
        self.frame_filtros.pack(pady=(10,5), padx=10, fill="x")

        # Frame para el título de la ventana
        self.frame_titulo = ctk.CTkFrame(self.frame_filtros,fg_color="#1DB1AC")
        self.frame_titulo.pack(padx=10,pady=10,fill="x",expand="True")
        self.label_titulo = ctk.CTkLabel(self.frame_titulo, text="Ponderaciones universidades de la Comunidad Valenciana 2025", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        self.frame_titulacion = ctk.CTkFrame(self.frame_filtros)
        self.frame_titulacion.pack(pady=(10,5), padx=10)
        ctk.CTkLabel(self.frame_titulacion, text="Titulación:", width=130).pack(side="left")
        self.degree_var = tk.StringVar()
        self.degree_combobox = ttk.Combobox(self.frame_titulacion, textvariable=self.degree_var, width=50)
        self.degree_combobox.pack(side="left", padx=10)
        self.frame_titulacion.pack(anchor="center")

        self.frame_universidad = ctk.CTkFrame(self.frame_filtros)
        self.frame_universidad.pack(pady=(5,5), padx=10)
        ctk.CTkLabel(self.frame_universidad, text="Universidad:", width=130).pack(side="left")
        self.university_var = tk.StringVar()
        self.university_combobox = ttk.Combobox(self.frame_universidad, textvariable=self.university_var, width=30)
        self.university_combobox.pack(padx=10)
        self.frame_universidad.pack(anchor="center")

        self.frame_asignatura = ctk.CTkFrame(self.frame_filtros)
        self.frame_asignatura.pack(pady=(5,5), padx=10)
        ctk.CTkLabel(self.frame_asignatura, text="Asignatura:", width=130).pack(side="left")
        self.subject_var = tk.StringVar()
        self.subject_combobox = ttk.Combobox(self.frame_asignatura, textvariable=self.subject_var, width=30)
        self.subject_combobox.pack(padx=10)
        self.frame_asignatura.pack(anchor="center")

        # Asociar las funciones de actualización y filtrado a los cambios en los comboboxes
        self.subject_var.trace('w', self.update_degrees_by_subject)
        self.university_var.trace('w', self.update_degrees_by_university)
        self.degree_var.trace('w', self.update_universities_and_subjects_by_degree)
        self.degree_var.trace('w', self.filter_subjects)
        self.university_var.trace('w', self.filter_subjects)
        self.subject_var.trace('w', self.filter_subjects)

        self.frame_botones_centrados = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_botones_centrados.pack(padx=10,pady=10)
        # Crear el botón de resetear filtros
        self.reset_button = ctk.CTkButton(self.frame_botones_centrados, text="Resetear Filtros", command=self.reset_filters,fg_color="#A88E28", hover_color="#5C5C2E")
        self.reset_button.pack(pady=(10,5),side="left")

        # Botón para cerrar la aplicación
        self.close_button = ctk.CTkButton(self.frame_botones_centrados, text="Cerrar", command=self.root.destroy, fg_color="#6F4257", hover_color="#533141")
        self.close_button.pack(padx=20,pady=(10,5),side="left")
        
        self.frame_botones_centrados.pack(anchor="center")
        
        self.frame_ponderaciones = ctk.CTkFrame(root)
        self.frame_ponderaciones.pack(pady=(10,5), padx=10, fill="both", expand=True)
        # Crear el treeview para mostrar los resultados
        columns = ('Asignatura', 'Ponderación')
        self.tree = ttk.Treeview(self.frame_ponderaciones, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Actualizar los valores de los comboboxes al iniciar la aplicación
        self.update_comboboxes()
    
    def leer_json(self):
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, 'assets', 'ponderaciones.json')
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    
    def update_comboboxes(self):
        degrees = set(self.data_ponderaciones.keys())
        universities = set()
        subjects = set()

        for details in self.data_ponderaciones.values():
            universities.update(details['universities'])
            subjects.update(details['subjects'].keys())

        self.degree_combobox['values'] = sorted(degrees)
        self.university_combobox['values'] = sorted(universities)
        self.subject_combobox['values'] = sorted(subjects)

    def update_degrees_by_subject(self, *args):
        subject = self.subject_var.get()
        if subject:
            degrees = [deg for deg, details in self.data_ponderaciones.items() if subject in details['subjects']]
            self.degree_combobox['values'] = sorted(degrees)
            self.show_degree_column()
        else:
            self.update_comboboxes()

    def update_degrees_by_university(self, *args):
        university = self.university_var.get()
        if university:
            degrees = [deg for deg, details in self.data_ponderaciones.items() if university in details['universities']]
            self.degree_combobox['values'] = sorted(degrees)
            self.show_degree_column()
        else:
            self.update_comboboxes()

    def update_universities_and_subjects_by_degree(self, *args):
        degree = self.degree_var.get()
        if degree:
            universities = set(self.data_ponderaciones[degree]['universities'])
            subjects = set(self.data_ponderaciones[degree]['subjects'].keys())
            self.university_combobox['values'] = sorted(universities)
            self.subject_combobox['values'] = sorted(subjects)
            self.hide_degree_column()
        else:
            self.update_comboboxes()

    def filter_subjects(self, *args):
        degree = self.degree_var.get()
        university = self.university_var.get()
        subject = self.subject_var.get()

        results = []

        for deg, details in self.data_ponderaciones.items():
            if degree and degree != deg:
                continue
            if university and university not in details['universities']:
                continue
            for subj, weight in details['subjects'].items():
                if subject and subject != subj:
                    continue
                results.append((subj, weight, deg))

        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar nuevos datos en el treeview
        for res in results:
            self.tree.insert('', 'end', values=res)
        
        # Actualizar los headers del treeview
        if degree:
            self.hide_degree_column()
        else:
            self.show_degree_column()

    def reset_filters(self):
        self.degree_var.set('')
        self.university_var.set('')
        self.subject_var.set('')
        
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.update_comboboxes()
        self.show_degree_column()

    def show_degree_column(self):
        self.tree["columns"] = ('Asignatura', 'Ponderación', 'Titulación')
        self.tree.heading('Asignatura', text='Asignatura')
        self.tree.heading('Ponderación', text='Ponderación')
        self.tree.heading('Titulación', text='Titulación')

    def hide_degree_column(self):
        self.tree["columns"] = ('Asignatura', 'Ponderación')
        self.tree.heading('Asignatura', text='Asignatura')
        self.tree.heading('Ponderación', text='Ponderación')

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        # Crear la ventana principal
        self.root.geometry("800x810+200+80")
        self.root.title("Simulador EBAU 2025")
        self.icon = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'assets', 'applogo.ico'))
        self.root.iconphoto(False, self.icon)
        
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
        self.corte = ctk.CTkToplevel(self.root)
        app2 = CorteApp(self.corte)
        self.corte.grab_set()
        
    def abre_ponderaciones(self):
        self.pondera = ctk.CTkToplevel(self.root)
        app1 = PonderacionesApp(self.pondera)
        self.pondera.grab_set()

if __name__ == "__main__":
    root = ctk.CTk()
    app = SimuladorApp(root)
    root.mainloop()