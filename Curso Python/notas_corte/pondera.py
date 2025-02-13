import tkinter as tk
from tkinter import ttk
import json
import customtkinter as ctk

# Cargar los datos JSON desde el archivo
with open('assets/ponderaciones.json', 'r') as f:
    data = json.load(f)

# Función para actualizar los valores de los comboboxes
def update_comboboxes():
    degrees = set(data.keys())
    universities = set()
    subjects = set()

    for details in data.values():
        universities.update(details['universities'])
        subjects.update(details['subjects'].keys())

    degree_combobox['values'] = sorted(degrees)
    university_combobox['values'] = sorted(universities)
    subject_combobox['values'] = sorted(subjects)

# Función para actualizar las titulaciones basadas en la asignatura seleccionada
def update_degrees_by_subject(*args):
    subject = subject_var.get()
    if subject:
        degrees = [deg for deg, details in data.items() if subject in details['subjects']]
        degree_combobox['values'] = sorted(degrees)
        show_degree_column()
    else:
        update_comboboxes()

# Función para actualizar las titulaciones basadas en la universidad seleccionada
def update_degrees_by_university(*args):
    university = university_var.get()
    if university:
        degrees = [deg for deg, details in data.items() if university in details['universities']]
        degree_combobox['values'] = sorted(degrees)
        show_degree_column()
    else:
        update_comboboxes()

# Función para actualizar las universidades y asignaturas basadas en la titulación seleccionada
def update_universities_and_subjects_by_degree(*args):
    degree = degree_var.get()
    if degree:
        universities = set(data[degree]['universities'])
        subjects = set(data[degree]['subjects'].keys())
        university_combobox['values'] = sorted(universities)
        subject_combobox['values'] = sorted(subjects)
        hide_degree_column()
    else:
        update_comboboxes()

# Función para filtrar y mostrar las asignaturas según los criterios seleccionados
def filter_subjects(*args):
    degree = degree_var.get()
    university = university_var.get()
    subject = subject_var.get()

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
    for item in tree.get_children():
        tree.delete(item)

    # Insertar nuevos datos en el treeview
    for res in results:
        tree.insert('', 'end', values=res)
    
    # Actualizar los headers del treeview
    if degree:
        hide_degree_column()
    else:
        show_degree_column()

# Función para resetear los filtros y limpiar el treeview
def reset_filters():
    degree_var.set('')
    university_var.set('')
    subject_var.set('')
    
    # Limpiar el treeview
    for item in tree.get_children():
        tree.delete(item)
    
    update_comboboxes()
    show_degree_column()

# Función para mostrar la columna de titulación
def show_degree_column():
    tree["columns"] = ('Asignatura', 'Ponderación', 'Titulación')
    tree.heading('Asignatura', text='Asignatura')
    tree.heading('Ponderación', text='Ponderación')
    tree.heading('Titulación', text='Titulación')

# Función para ocultar la columna de titulación
def hide_degree_column():
    tree["columns"] = ('Asignatura', 'Ponderación')
    tree.heading('Asignatura', text='Asignatura')
    tree.heading('Ponderación', text='Ponderación')


# Crear la ventana principal
root = ctk.CTk()
root.title("Tabla de Ponderaciones")
root.geometry("800x600")

frame_filtros= ctk.CTkFrame(root)
frame_filtros.pack(pady=(10,5), padx=10, fill="x")

label_titulo=ctk.CTkLabel(frame_filtros, text="Ponderaciones universidades de la Comunidad Valenciana", font=("Arial", 20, "bold"),text_color="#A2B4F5")
label_titulo.pack(pady=20)

frame_titulacion = ctk.CTkFrame(frame_filtros)
frame_titulacion.pack(pady=(10,5), padx=10)
# Crear los campos de entrada y etiquetas
ctk.CTkLabel(frame_titulacion, text="Titulación:", width=130).pack(side="left")
degree_var = tk.StringVar()
degree_combobox = ttk.Combobox(frame_titulacion, textvariable=degree_var, width=50)
degree_combobox.pack(side="left", padx=10)
frame_titulacion.pack(anchor="center")

frame_universidad = ctk.CTkFrame(frame_filtros)
frame_universidad.pack(pady=(5,5), padx=10)
ctk.CTkLabel(frame_universidad, text="Universidad:", width=130).pack(side="left")
university_var = tk.StringVar()
university_combobox = ttk.Combobox(frame_universidad, textvariable=university_var,width=30)
university_combobox.pack(padx=10)
frame_universidad.pack(anchor="center")

frame_asignatura = ctk.CTkFrame(frame_filtros)
frame_asignatura.pack(pady=(5,5), padx=10)
ctk.CTkLabel(frame_asignatura, text="Asignatura:", width=130).pack(side="left")
subject_var = tk.StringVar()
subject_combobox = ttk.Combobox(frame_asignatura, textvariable=subject_var,width=30)
subject_combobox.pack(padx=10)
frame_asignatura.pack(anchor="center")


# Asociar las funciones de actualización y filtrado a los cambios en los comboboxes
subject_var.trace('w', update_degrees_by_subject)
university_var.trace('w', update_degrees_by_university)
degree_var.trace('w', update_universities_and_subjects_by_degree)
degree_var.trace('w', filter_subjects)
university_var.trace('w', filter_subjects)
subject_var.trace('w', filter_subjects)

# Crear el botón de resetear filtros
reset_button = ctk.CTkButton(frame_filtros, text="Resetear Filtros", command=reset_filters)
reset_button.pack(pady=(10,5))

frame_ponderaciones = ctk.CTkFrame(root)
frame_ponderaciones.pack(pady=(10,5), padx=10, fill="both", expand=True)
# Crear el treeview para mostrar los resultados
columns = ('Asignatura', 'Ponderación')
tree = ttk.Treeview(frame_ponderaciones, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10, fill="both", expand=True)


# Actualizar los valores de los comboboxes al iniciar la aplicación
update_comboboxes()

# Ejecutar la aplicación
root.mainloop()