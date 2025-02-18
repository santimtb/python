import tkinter as tk
from tkinter import ttk
import json
import customtkinter as ctk
import os

def leer_json():
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, 'assets', 'ponderaciones.json')
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

# Configurar apariencia y tema
ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # Tema de colores

class PonderacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabla de Ponderaciones")
        self.root.geometry("800x600")

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
        self.close_button = ctk.CTkButton(self.frame_botones_centrados, text="Cerrar", command=root.quit, fg_color="#6F4257", hover_color="#533141")
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

    def update_comboboxes(self):
        degrees = set(data_ponderaciones.keys())
        universities = set()
        subjects = set()

        for details in data_ponderaciones.values():
            universities.update(details['universities'])
            subjects.update(details['subjects'].keys())

        self.degree_combobox['values'] = sorted(degrees)
        self.university_combobox['values'] = sorted(universities)
        self.subject_combobox['values'] = sorted(subjects)

    def update_degrees_by_subject(self, *args):
        subject = self.subject_var.get()
        if subject:
            degrees = [deg for deg, details in data_ponderaciones.items() if subject in details['subjects']]
            self.degree_combobox['values'] = sorted(degrees)
            self.show_degree_column()
        else:
            self.update_comboboxes()

    def update_degrees_by_university(self, *args):
        university = self.university_var.get()
        if university:
            degrees = [deg for deg, details in data_ponderaciones.items() if university in details['universities']]
            self.degree_combobox['values'] = sorted(degrees)
            self.show_degree_column()
        else:
            self.update_comboboxes()

    def update_universities_and_subjects_by_degree(self, *args):
        degree = self.degree_var.get()
        if degree:
            universities = set(data_ponderaciones[degree]['universities'])
            subjects = set(data_ponderaciones[degree]['subjects'].keys())
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

        for deg, details in data_ponderaciones.items():
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

if __name__ == "__main__":
    data_ponderaciones = leer_json()
    pondera = ctk.CTk()
    app1 = PonderacionesApp(pondera)
    pondera.mainloop()