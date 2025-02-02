import tkinter as tk
from tkinter import font

root = tk.Tk()
fuentes = list(font.families())
for f in fuentes:
    print(f)
root.mainloop()