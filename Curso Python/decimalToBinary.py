binario = []

while True:
    try:
        decimal = int(input("Introduce un número en el Sistema Decimal: ")) 
        break
    except ValueError:
        print("Debes introducir un número válido")

i=0

while (decimal // 2) >= 1:
    i += 1
    print(f"Iteración {i}: dividendo={decimal}")
    binario.append(decimal % 2)
    decimal = decimal // 2
binario.append(1)

bin=""

for val in list(reversed(binario)):
    bin+=str(val)

print(f"El número binario es: {bin}")
print(f"El número binario es: {list(reversed(binario))}")