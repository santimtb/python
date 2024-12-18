from tkinter import *

ventana = Tk()
ventana.title("Primera Ventana")
ventana.geometry("400x300")
menuBar=Menu(ventana)
ventana.config(bg="cornsilk2", menu=menuBar)

archivoMenu = Menu(menuBar)

archivoMenu.add_command(label="Nuevo")
archivoMenu.add_command(label="Abrir")
archivoMenu.add_command(label="Guardar")
archivoMenu.add_separator()
archivoMenu.add_command(label="Salir",command=ventana.quit)

menuBar.add_cascade(label="Archivo",menu=archivoMenu)

nombre = StringVar()
apellidos = StringVar()
saludo = StringVar()

nombre.set("Escribe aquí tu nombre")
apellidos.set("Escribe aquí tus apellidos")

def saludar():
    saludo.set("Hola "+nombre.get()+" "+apellidos.get())

etiqueta1 = Label(ventana, text="Nombre", bd=4, font="Courier 10")
etiqueta1.place(x=10,y=10)
etiqueta2 = Label(ventana, text="Apellidos")
etiqueta2.place(x=10,y=40)
entrada1=Entry(ventana, textvariable=nombre, bd=3)
entrada1.place(x=140,y=10)
entrada2=Entry(ventana, textvariable=apellidos, bd=3)
entrada2.place(x=140,y=40)

boton1=Button(ventana, text="Salir", command=ventana.destroy, bd=3)
boton1.place(x=10, y=100)

boton2=Button(ventana, text="Saludar", command=saludar, bd=3)
boton2.place(x=100, y=100)

entrada3=Entry(ventana, bd=10, textvariable=saludo, state="disabled")
entrada3.place(x=70,y=221)

ventana.mainloop()