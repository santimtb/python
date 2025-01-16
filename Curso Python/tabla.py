print("Vamos a desarrollar la Tabla de multiplicar que quieras...")
while True:
    try:
        tabla = int(input("Qué tabla de multiplicar quieres desarrollar? "))
        if tabla<0:
            raise Exception("La tabla debe ser un valor entero positivo")
        break
    except ValueError:
        print("Debes de introducir un valor numérico válido")
    except Exception as e:
        print(e)
        
for n in range(1,11):
    print(str(tabla),"x",str(n),"=",str(tabla*n))
    
print(f"{tabla} x {n} = {tabla*n}")