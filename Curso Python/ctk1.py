# This code is generated by PyUIbuilder: https://github.com/PaulleDemon/PyUIBuilder

import customtkinter as ctk

main = ctk.CTk()
main.configure(fg_color="#23272D")
main.title("Main Window")

frame = ctk.CTkFrame(main)
frame.configure(fg_color="#c26868")
frame.pack(side=ctk.LEFT, padx=10, pady=10, anchor='nw')

label = ctk.CTkLabel(master=frame, text="Simulador EBAU")
label.configure(fg_color="#E4E2E2", text_color="#000", height=40)
label.pack(side=ctk.TOP, padx=10, pady=10, anchor='center')

label1 = ctk.CTkLabel(master=frame, text="Comunidad Valenciana")
label1.configure(fg_color="#E4E2E2", text_color="#000", height=40)
label1.pack(side=ctk.TOP, padx=10, pady=10, anchor='center')


main.mainloop()