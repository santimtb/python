#Algoritmo para calcular un número combinatorio de m en n

def factorial(n):
    fact=1
    while n>1:
        fact=fact*n
        n-=1
    return fact

def combinatorio(m,n):
    return factorial(m)/(factorial(n)*factorial(m-n))

while True:
    try:
        m=int(input("Introduce el valor de m: "))
        if m<1:
            raise ValueError("El valor de m debe ser mayor o igual que 1")
        n=int(input("Introduce el valor de n: "))
        if n<0:
            raise ValueError("El valor de n debe ser mayor o igual que 0")
        if m<n:
            raise ValueError("El valor de m debe ser mayor o igual que n")
        break
    except ValueError as e:
        print(f"Valor incorrecto: {e}")

print(int(combinatorio(m,n)))