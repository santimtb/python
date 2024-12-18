import tkinter as tk
from matplotlib.pyplot import *
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from math import *

win = tk.Tk()
win.title("Gráfica de una función")
win.geometry("900x800")

style.use("fivethirtyeight")

figura = Figure()
ax = figura.add_subplot(111)

cvs=FigureCanvasTkAgg(figura,win)
cvs.draw()
cvs.get_tk_widget().pack(side="top",fill="both",expand=1)
tlb=NavigationToolbar2Tk(cvs,win)
tlb.update()
cvs.get_tk_widget().pack(side="top",fill="both",expand=1)

#Rangos
rang1=False
rang2=""
rang3=""

fun={"sin":"np.sin","cos":"np.cos","tan":"np.tan","sqrt":"np.sqrt","exp":"np.exp","log":"np.log","pi":"np.pi"}

def reemplaza(p):
    for i in fun:
        if i in p:
            p=p.replace(i,fun[i])
            return p
    return p
    
def animate(i):
    global rang1
    global rang2
    global rang3
    if rang1==True:
        try:
            min=float(rang3[0]);max=float(rang3[1])
            if min<max:
                x=np.arange(min,max,0.01)
                rang2=[min,max]
            else:
                rang1=False
        except:
            tk.messagebox.showwarning(message="El rango es incorrecto")
            rang1=False
            entra_var.delete(0,len(entra_var.get()))
    else:
        if rang2!="":
            x=np.arange(rang2[0],rang2[1],0.01)
        else:
            x=np.arange(0,10,0.01)
    try:
        sl = eval(graf_dt)
        ax.clear()
        ax.plot(x,sl)
    except:
        ax.plot()
    ax.axhline(0,color="gray")
    ax.axvline(0,color="gray")

    ani.event_source.stop()

def represent():
    global graf_dt
    global rang3
    global rang1

    tx_origl=entra_func.get()
    if entra_var.get()!="":
        rann=entra_var.get()
        rang3=rann.split(",")
        rang1=True
    graf_dt=reemplaza(tx_origl)
    ani.event_source.start()

ani=anim.FuncAnimation(figura,animate,interval=1000)
show()

entra_func = tk.Entry(win,width=60)
entra_var = tk.Entry (win, width=60)
botttt1 = tk.Button(win,text="Gráfica",command=represent)
botttt1.pack(side="bottom")
entra_var.pack(side="right")
entra_func.pack(side="bottom")

win.mainloop()