import requests

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYW50aW1lZGluYTUwQGdtYWlsLmNvbSIsImp0aSI6ImMzZmNhMzM4LTczYzQtNDJjMC1hZWIyLTNmNWM1NTVmNzg1MiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzMwMDU3MDE0LCJ1c2VySWQiOiJjM2ZjYTMzOC03M2M0LTQyYzAtYWViMi0zZjVjNTU1Zjc4NTIiLCJyb2xlIjoiIn0.2cRUZjFy__bbavdxcr6C60lvyya4F2kAUtUvV9_nTnQ"}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)