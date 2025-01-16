
while True:
    try:
        base = float(input("Introduce el valor de la base: "))
        if base<0:
            raise Exception("El valor debe ser positivo")
        break
    except ValueError:
        print("Debes introducir un valor numérico correcto")
    except Exception as e:
        print(e)
        
altura = int(input("Introduce el valor de la altura: "))

print("El Área del Triángulo es:",str(base*altura/2),"cm²")