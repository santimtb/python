billetes = (500,200,100,50,20,10,5)
monedas = (2,1,0.5,0.2,0.1,0.05,0.02,0.01)

while True:
    try:
        precio = float(input("Introduce la cantidad a cambiar: "))
        break
    except ValueError:
        print("Debes introducir un número válido")

for valor in billetes:
    if precio // valor:
        print(f"Billetes de {valor}: {int(precio // valor)}")
        precio=round(precio % valor,2)

for valor in monedas:
    if precio // valor:
        print(f"Monedas de {valor}: {int(precio // valor)}")
        precio=round(precio % valor,2)