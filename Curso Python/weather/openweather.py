import requests        #pip install requests
import time
from datetime import datetime

API = 'https://api.openweathermap.org/data/2.5/weather?q=Torrent&appid=48a3dd691689b68e49d4c40f21b447a8'  
weather=[]
try:
    json_datos = requests.get(API).json()
    print("El tiempo en: " +  json_datos['name'] + ' - '+ json_datos['sys']['country'] )
    print("Situación general: " + json_datos['weather'][0]['main'])
    print("Temperatura actual: " + str(int(json_datos['main']['temp'] - 273.15)) + " °C")
    print("temp_min: " + str(int(json_datos['main']['temp_min'] - 273.15))  +" °C")
    print("temp_max: " + str(int(json_datos['main']['temp_max'] - 273.15)) +" °C")
    print("presion: " + str(json_datos['main']['pressure']) + ' hPa')
    print("humedad: " + str(json_datos['main']['humidity']) + ' %')
    print("viento: " + str(int(json_datos['wind']['speed'])*18/5) + ' km/h')
    print("Amanecer: " + str(datetime.fromtimestamp(json_datos['sys']['sunrise'])))
    print("Anochecer: " + str(datetime.fromtimestamp(json_datos['sys']['sunset'])))
except:
    print('Error')

	