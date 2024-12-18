import requests
from PIL import Image
from io import BytesIO

CITY = "Torrent"
API_KEY = "48a3dd691689b68e49d4c40f21b447a8"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

print(url)

try:
    # Realizar la solicitud GET a la API
    respuesta = requests.get(url)
    respuesta.raise_for_status()  # Lanza una excepción si hay un error HTTP

    # Analizar la respuesta JSON
    data = respuesta.json()

    # Verificar si se encontraron resultados
    if data:
        print(f"Temperatura: {data['main']['temp']}°C")
        print(f"Clima General: {data['weather'][0]['description']}")
        print(f"Humedad: {data['main']['humidity']}%")
        print(f"Velocidad del viento: {data['wind']['speed']*3.6:.2f} km/h")
        print(f"Sensación térmica: {data['main']['feels_like']}")
        image_url = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']+'@4x.png'}"
        print(image_url)
        try:
            # Descargar la imagen
            response = requests.get(image_url)
            response.raise_for_status()  # Verifica que no haya errores en la descarga

            # Cargar la imagen en memoria
            image = Image.open(BytesIO(response.content))

            # Mostrar la imagen
            image.show()

        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen: {e}")
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
    else:
                print("No se encontraron resultados para la ciudad especificada.")

except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API: {e}")
