import tkinter as tk
from PIL import Image  #pip install Pillow
import requests        #pip install requests
import time
import os
from dotenv import load_dotenv #pip install python-dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

ventana = tk.Tk()
ventana.title('Predicción del tiempo')
ventana.config(bg='white')
ventana.minsize(height= 300,width=500)

frame_titulo = tk.Frame(ventana, height=50,bg='#FF5733')
frame_titulo.pack(anchor="n",fill='x', padx=10,pady=10,expand='yes')

label = tk.Label(frame_titulo, text="Frame Superior", bg="lightblue")
label.pack(pady=10)
ventana.mainloop()