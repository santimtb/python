import tkinter as tk
from tkinter import ttk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Multiventana")
        self.geometry("300x200")

        # Botón para abrir la segunda ventana
        btn_open_window = ttk.Button(self, text="Abrir Segunda Ventana", command=self.open_second_window)
        btn_open_window.pack(pady=20)

    def open_second_window(self):
        self.attributes("-disabled", True)  # Deshabilita la ventana principal
        second_window = SecondWindow(self)
        second_window.grab_set()  # Hace que la ventana sea modal
        second_window.attributes("-topmost", True)  # Mantiene la ventana en primer plano

class SecondWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Segunda Ventana")
        self.geometry("300x200")

        # Etiqueta en la segunda ventana
        lbl = ttk.Label(self, text="¡Hola desde la segunda ventana!")
        lbl.pack(pady=20)

        # Botón para cerrar la ventana
        btn_close = ttk.Button(self, text="Cerrar", command=self.on_close)
        btn_close.pack(pady=20)

    def on_close(self):
        self.master.attributes("-disabled", False)  # Habilita la ventana principal
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()