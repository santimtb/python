# String que contiene la multiplicación
expresion = "12x34"

# Dividir el string usando el símbolo 'x' como separador
terminos = expresion.split('x')

# Extraer los dos términos
termino1 = int(terminos[0])  # Convertir a entero (si es necesario)
termino2 = int(terminos[1])  # Convertir a entero (si es necesario)

# Imprimir los resultados
print("Primer término:", termino1)
print("Segundo término:", termino2)