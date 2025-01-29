def calcular_precio_por_alumno(num_alumnos, precio_actividad,  precio_bus):
    costo_actividad = precio_actividad * num_alumnos
    costo_total = costo_actividad + precio_bus
    precio_por_alumno = costo_total / num_alumnos

    return round(precio_por_alumno, 2)

# Ejemplo de uso:
precio_actividad = float(input("Ingrese el precio de la actividad por alumno: "))
precio_bus = float(input("Ingrese el precio del autobús: "))
while True:
    num_alumnos = int(input("Ingrese el número de alumnos que asistirán [0 para salir]: "))
    if num_alumnos == 0:
        break
    else:
        print(f"El precio por alumno es: {calcular_precio_por_alumno(num_alumnos,precio_actividad,precio_bus)} €")