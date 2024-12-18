import requests
from dotenv import load_dotenv
import os

# Carga las variables de entorno del archivo .env
load_dotenv()

api_key = os.getenv('API_KEY')

# Where USD is the base currency you want to use
url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR'
print(url)
# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)
			