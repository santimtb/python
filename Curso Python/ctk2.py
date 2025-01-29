from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.icons import Icon

root = tb.Window(themename="superhero")

root.title("TTK Bootstrap Icons!!!")
#root.iconbitmap('images/codemy.ico')
root.geometry("500x550")

img = PhotoImage(data=Icon.house-fill)

#Label
my_label = tb.Label(image=img)
my_label.pack(pady=40)

root.mainloop()