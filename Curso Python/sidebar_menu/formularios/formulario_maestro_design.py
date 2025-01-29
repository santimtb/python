import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import os

class FormularioMaestroDesign(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logo = self.leer_imagen("./imagenes/logo.png", (560, 136))
        self.perfil = self.leer_imagen("./imagenes/Perfil.png", (100, 100))
        self.COLOR_BARRA_SUPERIOR = "#1F2329"
        self.COLOR_MENU_LATERAL = "#2A3138"
        self.COLOR_CUERPO_PRINCIPAL = "#F1FAFF"
        self.COLOR_MENU_CURSOR_ENCIMA = "#2F88C5"
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
    
    def config_window(self):
        #configuracion inicial de la ventana
        self.title("Formulario Maestro - Python GUI con TKinter")
        self.configure(bg=self.COLOR_CUERPO_PRINCIPAL)
        self.resizable(False, False)
        #self.iconbitmap("./imagenes/logo.ico")
        w, h = 1024, 600
        self.centrar_ventana(w, h)

    def paneles(self):
        #barra superior
        self.barra_superior = tk.Frame(self, bg=self.COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP,fill="both")
        #menu lateral
        self.menu_lateral = tk.Frame(self, bg=self.COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill="both", expand=False)
        #Cuerpo principal
        self.cuerpo_principal = tk.Frame(self, bg=self.COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill="both", expand=True)
        

    def controles_barra_superior(self):
        font_awesome = font.Font(family="FontAwesome", size=12)
        #Botón del menu lateral
        self.boton_menu = tk.Button(self.barra_superior, text="\uf0c9")
        self.boton_menu.config(font=font_awesome, bg=self.COLOR_BARRA_SUPERIOR, fg="white", bd=0, highlightthickness=0, padx=10)
        self.boton_menu.pack(side=tk.LEFT)

        self.labelTitulo = tk.Label(self.barra_superior, text="Formulario Maestro")
        self.labelTitulo.config(bg=self.COLOR_BARRA_SUPERIOR, fg="white", font=("Roboto", 15), padx=20,pady=10, width=16)    
        self.labelTitulo.pack(side=tk.LEFT)

        #Etiqueta de Info
        self.labelTitulo= tk.Label(self.barra_superior, text="Santi Medina")
        self.labelTitulo.config(bg=self.COLOR_BARRA_SUPERIOR,fg="white", font=("Roboto", 10), width=20, padx=10)   
        self.labelTitulo.pack(side=tk.RIGHT) 

    def centrar_ventana(self,aplicacion_ancho,aplicacion_alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = int((pantalla_ancho/2) - (aplicacion_ancho/2))
        y = int((pantalla_alto/2) - (aplicacion_alto/2))
        self.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")

    def leer_imagen(self, ruta, size):
        imagen = Image.open(ruta)
        imagen = imagen.resize(size, Image.ADAPTIVE)
        return ImageTk.PhotoImage(imagen)