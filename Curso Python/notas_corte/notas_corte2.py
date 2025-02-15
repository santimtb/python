import json
import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntry

# Cargar los datos del archivo JSON desde la subcarpeta "assets"
with open('assets/titulaciones.json', 'r') as file:
    data = json.load(file)

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

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Notas de Corte")
        self.root.geometry("800x600")
        self.root.config(bg="#374369")

        # Crear una lista de titulaciones, universidades y facultades para el autocompletado
        titulaciones = [item['Titulación'] for item in data]
        universidades = list(set(item['Universidad'] for item in data))
        facultades = list(set(item['Facultad'] for item in data))

        # Entry con autocompletado y marcador de posición
        #Creamos un Frame contenedor
        self.frame_titulacion = tk.Frame(root, bg="#374369")
        self.frame_titulacion.pack(fill="x",expand=True,padx=10,pady=10)
        # Frame para centrar los widgets
        self.frame_titulacion_widgets=tk.Frame(self.frame_titulacion, bg="#374369")
        self.frame_titulacion_widgets.pack()
        self.label_titulacion = tk.Label(self.frame_titulacion_widgets, text="Titulación:", font=("Verdana",14,"bold"), bg="#374369", fg="#FFE49C")
        self.label_titulacion.pack(side="left",padx=10,pady=10)
        self.entry_titulacion = AutocompleteEntryWithPlaceholder(self.frame_titulacion_widgets, completevalues=titulaciones, placeholder="Buscar Titulación", width=50)
        self.entry_titulacion.pack(side="left",padx=10,pady=10)
        self.frame_titulacion_widgets.pack(anchor="center")

        # Filtro por universidad y facultad
        # Creamos un Frame contenedor 
        self.frame_filtros = tk.Frame(root, bg="#374369")
        self.frame_filtros.pack(fill="x",expand=True,padx=10,pady=5)
        # Frame para centrar los widgets
        self.frame_filtros_widgets=tk.Frame(self.frame_filtros, bg="#374369")
        self.frame_filtros_widgets.pack()
        # Combobox para universidades
        self.combo_universidad = ttk.Combobox(self.frame_filtros_widgets, values=universidades)
        self.combo_universidad.pack(side="left",padx=10,pady=10)
        self.combo_universidad.set("Seleccionar Universidad")
        # Combobox para facultades
        self.combo_facultad = ttk.Combobox(self.frame_filtros_widgets, values=facultades)
        self.combo_facultad.pack(side="left", padx=10,pady=10)
        self.combo_facultad.set("Seleccionar Facultad")
        self.frame_filtros_widgets.pack(anchor="center")

        # Lista para mostrar resultados
        self.listbox = tk.Listbox(root, width=90)
        self.listbox.pack(pady=10)
        self.listbox.bind('<<ListboxSelect>>', self.show_details)

        # Diccionario para mapear índices de la Listbox a elementos de datos
        self.index_map = {}

        # Etiqueta para mostrar la nota de corte general
        self.label_general = tk.Label(root, text="", bg="#374369", fg="#B5E8BB", font=("Arial",16,"bold"))
        self.label_general.pack(pady=5)
        
        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TCheckbutton", 
            background="#374369",
            foreground="white",
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            padding=6
        )
        # Cambiar el color cuando el botón está seleccionado
        style.map("Custom.TCheckbutton",
            background=[("selected", "#374369"), ("active", "#374369")],  
            foreground=[("selected", "#F5D767"), ("active", "#F567F0"),("disabled", "gray")],  # Color cuando está deshabilitado
        )
        # Checkbutton para mostrar la nota de deportista de élite
        self.show_deportista_var = tk.BooleanVar()
        self.check_deportista = ttk.Checkbutton(root, text="Mostrar Nota Deportista", variable=self.show_deportista_var, command=self.update_details, style="Custom.TCheckbutton")
        self.check_deportista.pack(pady=5)

        # Etiqueta para mostrar la nota de deportista de élite
        self.label_deportista = tk.Label(root, text="", bg="#374369", fg="#F567F0", font=("Arial",16,"bold"))
        self.label_deportista.pack(pady=5)

        # Botón para resetear filtros
        self.reset_button = ttk.Button(root, text="Resetear Filtros", command=self.reset_filters)
        self.reset_button.pack(pady=5)

        # Botón para cerrar la aplicación
        self.close_button = ttk.Button(root, text="Cerrar", command=root.quit)
        self.close_button.pack(pady=5)

        # Vincular eventos
        self.entry_titulacion.bind('<KeyRelease>', self.apply_filters)
        self.combo_universidad.bind('<<ComboboxSelected>>', self.apply_filters)
        self.combo_facultad.bind('<<ComboboxSelected>>', self.apply_filters)

    def apply_filters(self, event=None):
        search_term = self.entry_titulacion.get().lower()
        if self.entry_titulacion.placeholder_active:
            search_term = ""
        selected_universidad = self.combo_universidad.get()
        selected_facultad = self.combo_facultad.get()

        self.listbox.delete(0, tk.END)
        self.index_map.clear()
        for index, item in enumerate(data):
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
            item = data[data_index]
            self.label_general.config(text=f"Nota de corte General: {item['General']}")
            self.selected_item = item
            self.update_details()

    def update_details(self):
        if hasattr(self, 'selected_item'):
            if self.show_deportista_var.get():
                self.label_deportista.config(text=f"Nota de corte Deportista de élite: {self.selected_item['Deportista']}")
            else:
                self.label_deportista.config(text="")

    def reset_filters(self):
        self.entry_titulacion.delete(0, tk.END)
        self.entry_titulacion.insert(0, self.entry_titulacion.placeholder)
        self.combo_universidad.set("Seleccionar Universidad")
        self.combo_facultad.set("Seleccionar Facultad")
        self.listbox.delete(0, tk.END)
        self.label_general.config(text="")
        self.label_deportista.config(text="")
        self.show_deportista_var.set(False)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()