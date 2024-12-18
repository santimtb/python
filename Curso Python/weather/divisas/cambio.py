import requests

api_key = 'abe92a0da5161d1cf50b9447'
# Where USD is the base currency you want to use
url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
print(url)
# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)
			