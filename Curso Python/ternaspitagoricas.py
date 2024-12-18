#Algoritmo para obtener ternas pitagóricas

def obtener_numero():
    while True:
        try:
            iteraciones = int(input("Introduce el número de ternas pitagóricas que quieres obtener: "))
            if iteraciones<2:
                raise ValueError("El valor debe ser mayor de 1")
            return iteraciones
        except ValueError as e:
            print(f"Valor incorrecto: {e}")

i=obtener_numero()
p=0

for m in range(2,i+2):
    for n in range(1,m):
        if (m > n):
            a = m**2 - n**2
            b = 2 * m * n
            c = m ** 2 + n ** 2
            p+=1
            print(str(p)+". ("+str(a)+","+str(b)+","+str(c)+")")
            if (p==i):
                break
    if (p==i):
        break