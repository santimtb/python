
from pydub import AudioSegment
from pydub.playback import play
import requests
from io import BytesIO

paises = ['uk', 'us', 'au']

paises_literales={
    'uk': 'Reino Unido',
    'us': 'Estados Unidos',
    'au': 'Australia'
}

palabra = input("Introduce una palabra en inglés: ")
# URL de la API de diccionario
url_api = f"https://api.dictionaryapi.dev/api/v2/entries/en/{palabra}"
# Realizar la solicitud a la API
response = requests.get(url_api)
if response.status_code == 200:
    data = response.json()
    print(f"Word: {data[0]['word']}")
    print(f"Phonetic: {data[0]['phonetic']}")
    i = 1
    for phonetic in data[0]['phonetics']:
        print(f"Phonetic Text {i}: {phonetic['text']}")
        if phonetic['audio']!= "":
            for pais in paises:
                if f"-{pais}" in phonetic['audio']:
                    print(f"Pronunciación en {paises_literales[pais]}: {phonetic['audio']}")
                    break
            resp = input("¿Quieres escuchar la pronunciación? (S/n): ")
            if resp in ['S', 's', 'si', 'Si', 'SI', '']:
                # Reproducir el audio
                print("Reproduciendo audio...")
                # Obtener la URL de la pronunciación
                audio_url = phonetic['audio']
                print(f"URL de pronunciación: {audio_url}")
                response_audio = requests.get(audio_url)
                print("Cargando el archivo MP3...")
                # Descargar el archivo MP3
                audio_data = BytesIO(response_audio.content)
                # Cargar el archivo MP3 en un objeto AudioSegment
                audio = AudioSegment.from_file(audio_data, format="mp3")
                # Reproducir el archivo MP3
                play(audio)
        else:
            print("No se encontró el audio de la pronunciación para esta palabra.")
        i+=1
    for significado in data[0]['meanings']:
        print(f"Parte del habla: {significado['partOfSpeech']}")
        for definicion in significado['definitions']:
            print(f"Definición: {definicion['definition']}")
            if 'example' in definicion:
                print(f"Ejemplo: {definicion['example']}")
            else:
                print("No hay ejemplo disponible.")
            if 'synonyms' in definicion:
                print(f"Sinónimos: {', '.join(definicion['synonyms'])}")    
            
else:
    print("Error al obtener la información de la palabra.")

