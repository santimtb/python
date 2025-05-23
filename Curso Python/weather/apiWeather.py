# Aplicacion Meteorológica  ----> https://www.youtube.com/watch?v=fGRF7VODOOw&t=78s
# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren

from tkinter import  Tk, Button, Entry, Label,PhotoImage,Frame
from PIL import Image  #pip install Pillow
import requests        #pip install requests
import time
import os
from dotenv import load_dotenv #pip install python-dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

class Ventana(Frame):
	def __init__(self, master, *args):
		super().__init__(master,*args)
		self.click = True

		self.master.columnconfigure(0, weight=1)
		self.master.columnconfigure(1, weight=1)
		self.master.rowconfigure(1, weight=1)
		self.master.columnconfigure(2, weight=1)
		self.master.rowconfigure(2, weight=1)
		self.frame = Frame(self.master, bg='white', highlightbackground='deep pink',highlightthickness=2)
		self.frame.grid(columnspan=3, row = 0, sticky='nsew', padx=5, pady=5)
		self.frame2 = Frame(self.master, bg='pale green', highlightbackground='dark violet',highlightthickness=2)
		self.frame2.grid(column=0, row = 1, sticky='nsew', padx=5, pady=5)
		self.frame3 = Frame(self.master, bg='SeaGreen1', highlightbackground='dark violet',highlightthickness=2) #pink
		self.frame3.grid(column=1, row = 1, sticky='nsew', padx=5, pady=5)
		self.frame4 = Frame(self.master, bg='PaleTurquoise1', highlightbackground='dark violet',highlightthickness=2)
		self.frame4.grid(column=2, row = 1, sticky='nsew', padx=5, pady=5)
		self.frame5 = Frame(self.master, bg='cyan2', highlightbackground='dark violet',highlightthickness=2) #light coral
		self.frame5.grid(column=0, row = 2, sticky='nsew', padx=5, pady=5)
		self.frame6 = Frame(self.master, bg='aquamarine', highlightbackground='dark violet',highlightthickness=2)
		self.frame6.grid(column=1, row = 2, sticky='nsew', padx=5, pady=5)
		self.frame7 = Frame(self.master, bg='sky blue', highlightbackground='dark violet',highlightthickness=2) #HotPink1
		self.frame7.grid(column=2, row =2 , sticky='nsew', padx=5, pady=5)

		self.widgets()

	def animacion(self):
		self.frame.config(highlightbackground='red')
		self.frame2.config(highlightbackground='red')
		self.frame3.config(highlightbackground='red')
		self.frame4.config(highlightbackground='red')
		self.frame5.config(highlightbackground='red')
		self.frame6.config(highlightbackground='red')
		self.frame7.config(highlightbackground='red')
		self.obtener_tiempo()
		gif = Image.open('img/buscar.gif')
		frames = gif.n_frames
		if self.click == True:
			for i in range(1, frames):
				self.inicio = PhotoImage(file ='img/buscar.gif', format='gif -index %i' %(i))
				self.bt_inicio['image'] = self.inicio
				time.sleep(0.04)
				self.master.update()
				self.click= False
				if i + 1 == frames:
					self.click = True

	def obtener_tiempo(self,event):
		ciudad = self.ingresa_ciudad.get()
		api_key = os.getenv('API_KEY')
		url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es'.format(ciudad)
		try:
			json_datos = requests.get(url).json()
			self.temp['text'] = str(int(json_datos['main']['temp'])) + " °C"
			self.temp_min['text'] = str(int(json_datos['main']['temp_min']))  +" °C"
			self.temp_max['text'] = str(int(json_datos['main']['temp_max'])) +" °C"
			self.presion['text'] = str(json_datos['main']['pressure']) + ' hPa'
			self.humedad['text'] = str(json_datos['main']['humidity']) + ' %'
			self.viento['text'] = str(int(json_datos['wind']['speed'])*18/5) + ' km/h'
			self.localidad['text'] =  json_datos['name'] + ' - '+ json_datos['sys']['country']
			print(json_datos)
		except:
			self.aviso['text'] =  'Error'
			self.temp['text'] = '-'
			self.temp_min['text'] = '-'
			self.temp_max['text'] = '-'
			self.presion['text'] = '-'
			self.humedad['text'] = '-'
			self.viento['text'] = '-'
			self.master.update()
			time.sleep(1)
			self.aviso['text'] = ''
			self.localidad['text'] = ''

	def widgets(self):
		self.inicio = PhotoImage(file ='img/buscar.gif')
		self.imagen_temp = PhotoImage(file ='img/temperatura.png')
		self.imagen_temp_min = PhotoImage(file ='img/temp_min.png')
		self.imagen_temp_max = PhotoImage(file ='img/temp_max.png')
		self.imagen_humedad = PhotoImage(file ='img/humedad.png')
		self.imagen_viento = PhotoImage(file ='img/viento.png')
		self.imagen_presion = PhotoImage(file ='img/presion.png')
		self.bt_inicio = Button(self.frame, image= self.inicio, bg='red',highlightthickness=0, activebackground='white', bd=0, command = self.animacion)
		self.bt_inicio.grid(column=0, row=0, padx=2, pady=2)
		self.ingresa_ciudad = Entry(self.frame, font=('Comic Sans MS', 12),highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=2)
		self.ingresa_ciudad.grid(column=1,row=0)
		self.ingresa_ciudad.bind('<Return>',self.obtener_tiempo)
		Label(self.frame,text='Buscar',fg= 'gray55', bg='white',font=('Comic Sans MS',10)).grid(column=2,row=0, padx=5)
		self.aviso = Label(self.frame,fg= 'red2', bg='white',font=('Comic Sans MS',12))
		self.aviso.grid(column=3,row=0, padx=5)
		self.localidad = Label(self.frame,fg= 'magenta', bg='white',font=('Arial',12, 'bold'))
		self.localidad.grid(column=4,row=0, padx=5)

		Label(self.frame2,text='Temperatura', bg='pale green').pack(expand=True) #Kaufmann BT
		Label(self.frame3,text='Temperatura Maxima', bg='SeaGreen1').pack(expand=True)
		Label(self.frame4,text='Temperatura Minima' , bg='PaleTurquoise1').pack(expand=True)
		Label(self.frame5,text='Humedad' , bg='cyan2').pack(expand=True)
		Label(self.frame6,text='Viento' , bg='aquamarine').pack(expand=True)
		Label(self.frame7,text='Presión' , bg='sky blue').pack(expand=True)

		Label(self.frame2, image= self.imagen_temp, bg='pale green').pack(expand=True, side='left')
		Label(self.frame3, image= self.imagen_temp_max, bg='SeaGreen1').pack(expand=True, side='left')
		Label(self.frame4, image= self.imagen_temp_min, bg='PaleTurquoise1').pack(expand=True, side='left')
		Label(self.frame5, image= self.imagen_humedad, bg='cyan2').pack(expand=True, side='left')
		Label(self.frame6, image= self.imagen_viento, bg='aquamarine').pack(expand=True, side='left')
		Label(self.frame7, image= self.imagen_presion, bg='sky blue').pack(expand=True, side='left')

		self.temp = Label(self.frame2,  bg='pale green',font=('Impact',20))
		self.temp.pack(expand=True, side='right')
		self.temp_max = Label(self.frame3,bg='SeaGreen1',font=('Impact',20))
		self.temp_max.pack(expand=True, side='right')
		self.temp_min = Label(self.frame4, bg='PaleTurquoise1',font=('Impact',20))
		self.temp_min.pack(expand=True, side='right')
		self.humedad = Label(self.frame5, bg='cyan2',font=('Impact',20))
		self.humedad.pack(expand=True, side='right')
		self.viento = Label(self.frame6, bg='aquamarine',font=('Impact',20))
		self.viento.pack(expand=True, side='right')
		self.presion = Label(self.frame7, bg='sky blue',font=('Impact',20))
		self.presion.pack(expand=True, side='right')

	def first_focus(self):
		self.ingresa_ciudad.focus_set()

if __name__ == "__main__":
	#Cambiamos al directorio de trabajo actual
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	ventana = Tk()
	ventana.title('Predicción del tiempo')
	ventana.config(bg='white')
	ventana.minsize(height= 300,width=500)
	ventana.iconphoto(True,PhotoImage('img/temperatura.png'))
	#ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file='img/temperatura.png'))
	ventana.geometry('600x300+180+80')
	app = Ventana(ventana)
	app.after(0,app.first_focus)
	app.mainloop()

