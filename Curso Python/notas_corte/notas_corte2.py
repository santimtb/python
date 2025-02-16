import json
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntry

# Cargar los datos del archivo JSON desde la subcarpeta "assets"
with open('assets/titulaciones.json', 'r') as file:
    data = json.load(file)

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

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Notas de Corte")
        self.root.geometry("800x600")

        # Crear una lista de titulaciones, universidades y facultades para el autocompletado
        titulaciones = [item['Titulación'] for item in data]
        universidades = list(set(item['Universidad'] for item in data))
        facultades = list(set(item['Facultad'] for item in data))

        # Entry con autocompletado y marcador de posición
        #Creamos un Frame contenedor
        self.frame_titulacion = ctk.CTkFrame(root)
        self.frame_titulacion.pack(fill="x",expand=True,padx=10,pady=10)
        # Frame para centrar los widgets
        self.frame_titulacion_widgets=ctk.CTkFrame(self.frame_titulacion,fg_color="transparent")
        self.frame_titulacion_widgets.pack()
        self.label_titulacion = ctk.CTkLabel(self.frame_titulacion_widgets, text="Titulación:", font=("Verdana",14,"bold"))
        self.label_titulacion.pack(side="left",padx=10,pady=10)
        self.entry_titulacion = AutocompleteEntryWithPlaceholder(self.frame_titulacion_widgets, completevalues=titulaciones, placeholder="Buscar Titulación", width=50)
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
        self.close_button = ctk.CTkButton(self.frame_botones_centrados, text="Cerrar", command=root.quit, fg_color="#6F4257", hover_color="#533141")
        self.close_button.pack(padx=20,pady=5,side="left")

        self.frame_botones_centrados.pack(anchor="center")
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

def main():
    root = ctk.CTk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()