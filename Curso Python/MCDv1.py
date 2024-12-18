def mcd(a, b):
    while (b != 0) and (a !=0):
        if (a>b):
            a, b = b, a % b
        else:
            a, b = a, b % a
    return a

# Ejemplo de uso
num1 = 48
num2 = 64
print(f"El MCD de {num1} y {num2} es {mcd(num1, num2)}")
print(f"El mcm de {num1} y {num2} es {int(num1*num2/mcd(num1, num2))}")
