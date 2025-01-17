fase_general = ("Castellano: lengua y literatura", "Valenciano: lengua i literaura", "Lengua Extranjera", "Historia de España","Matemáticas")

def pide_nota(asignatura):
    while True:
        try:
            nota = float(input(f"Introduce la nota de {asignatura} (0-10): "))
            if not 0 <= nota <= 10:
                raise ValueError("La nota debe estar entre 0 y 10.")
            return nota
        except ValueError as e:
            print(f"Error: {e}")

def pide_ponderacion(asignatura):
    while True:
        try:
            ponderacion=float(input(f"Introduce la ponderación de {asignatura} (0.1 o 0.2): "))
            if ponderacion not in (0.1, 0.2):
                raise ValueError("La ponderación debe ser 0.1 o 0.2.")
            return ponderacion
        except ValueError as e:
            print(f"Error: {e}")
    
def notas_fase_general():
    notas=[]
    for asignatura in fase_general:
        nota = pide_nota(asignatura)
        notas.append((asignatura,nota))
    return notas

def notas_fase_especifica():
    notas=[]
    for i in range(2):
        nota = pide_nota(f"Optativa {i+1}")
        ponderacion = pide_ponderacion(f"Optativa {i+1}")
        notas.append((nota, ponderacion))

print("<<< Simulador de EBAU >>>")
#Obtenemos la nota media de Bachillerato
print("Nota Media de Bachillerato")
media_bachillerato = pide_nota("Bachillerato")
notas_general = notas_fase_general()
notas_especifica=notas_fase_especifica()

print(notas_general)
print(notas_general)
