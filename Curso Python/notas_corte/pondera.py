import tkinter as tk
from tkinter import ttk
import json
import customtkinter as ctk

# Cargar los datos JSON desde el archivo
with open('assets/ponderaciones.json', 'r') as f:
    data = json.load(f)

class PonderacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabla de Ponderaciones")
        self.root.geometry("800x600")

        frame_filtros = ctk.CTkFrame(root)
        frame_filtros.pack(pady=(10,5), padx=10, fill="x")

        label_titulo = ctk.CTkLabel(frame_filtros, text="Ponderaciones universidades de la Comunidad Valenciana", font=("Arial", 20, "bold"), text_color="#A2B4F5")
        label_titulo.pack(pady=20)

        frame_titulacion = ctk.CTkFrame(frame_filtros)
        frame_titulacion.pack(pady=(10,5), padx=10)
        ctk.CTkLabel(frame_titulacion, text="Titulación:", width=130).pack(side="left")
        self.degree_var = tk.StringVar()
        self.degree_combobox = ttk.Combobox(frame_titulacion, textvariable=self.degree_var, width=50)
        self.degree_combobox.pack(side="left", padx=10)
        frame_titulacion.pack(anchor="center")

        frame_universidad = ctk.CTkFrame(frame_filtros)
        frame_universidad.pack(pady=(5,5), padx=10)
        ctk.CTkLabel(frame_universidad, text="Universidad:", width=130).pack(side="left")
        self.university_var = tk.StringVar()
        self.university_combobox = ttk.Combobox(frame_universidad, textvariable=self.university_var, width=30)
        self.university_combobox.pack(padx=10)
        frame_universidad.pack(anchor="center")

        frame_asignatura = ctk.CTkFrame(frame_filtros)
        frame_asignatura.pack(pady=(5,5), padx=10)
        ctk.CTkLabel(frame_asignatura, text="Asignatura:", width=130).pack(side="left")
        self.subject_var = tk.StringVar()
        self.subject_combobox = ttk.Combobox(frame_asignatura, textvariable=self.subject_var, width=30)
        self.subject_combobox.pack(padx=10)
        frame_asignatura.pack(anchor="center")

        # Asociar las funciones de actualización y filtrado a los cambios en los comboboxes
        self.subject_var.trace('w', self.update_degrees_by_subject)
        self.university_var.trace('w', self.update_degrees_by_university)
        self.degree_var.trace('w', self.update_universities_and_subjects_by_degree)
        self.degree_var.trace('w', self.filter_subjects)
        self.university_var.trace('w', self.filter_subjects)
        self.subject_var.trace('w', self.filter_subjects)

        # Crear el botón de resetear filtros
        reset_button = ctk.CTkButton(frame_filtros, text="Resetear Filtros", command=self.reset_filters)
        reset_button.pack(pady=(10,5))

        frame_ponderaciones = ctk.CTkFrame(root)
        frame_ponderaciones.pack(pady=(10,5), padx=10, fill="both", expand=True)
        # Crear el treeview para mostrar los resultados
        columns = ('Asignatura', 'Ponderación')
        self.tree = ttk.Treeview(frame_ponderaciones, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Actualizar los valores de los comboboxes al iniciar la aplicación
        self.update_comboboxes()

    def update_comboboxes(self):
        degrees = set(data.keys())
        universities = set()
        subjects = set()

        for details in data.values():
            universities.update(details['universities'])
            subjects.update(details['subjects'].keys())

        self.degree_combobox['values'] = sorted(degrees)
        self.university_combobox['values'] = sorted(universities)
        self.subject_combobox['values'] = sorted(subjects)

    def update_degrees_by_subject(self, *args):
        subject = self.subject_var.get()
        if subject:
            degrees = [deg for deg, details in data.items() if subject in details['subjects']]
            self.degree_combobox['values'] = sorted(degrees)
            self.show_degree_column()
        else:
            self.update_comboboxes()

    def update_degrees_by_university(self, *args):
        university = self.university_var.get()
        if university:
            degrees = [deg for deg, details in data.items() if university in details['universities']]
            self.degree_combobox['values'] = sorted(degrees)
            self.show_degree_column()
        else:
            self.update_comboboxes()

    def update_universities_and_subjects_by_degree(self, *args):
        degree = self.degree_var.get()
        if degree:
            universities = set(data[degree]['universities'])
            subjects = set(data[degree]['subjects'].keys())
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

        for deg, details in data.items():
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

def main():
    root = ctk.CTk()
    app = PonderacionesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()