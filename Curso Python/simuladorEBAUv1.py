def pide_nota(asignatura):
    while True:
        try:
            nota = float(input(f"Introduce la nota de {asignatura} (0-10): "))
            if not 0 <= nota <= 10:
                raise ValueError("La nota debe estar entre 0 y 10.")
            return nota
        except ValueError as e:
            print(f"Error: {e}")
            print("Por favor, introduce un número válido entre 0 y 10.")

def calcular_nota_acceso():
    try:
        media_bachillerato = float(input("Introduce la nota media de Bachillerato (0-10): "))
        if not 0 <= media_bachillerato <= 10:
            raise ValueError("La nota media de Bachillerato debe estar entre 0 y 10.")

        notas_fase_general = []
        for i in range(4):
            while True:
                try:
                    nota = float(input(f"Introduce la nota de la asignatura {i+1} de la fase general (0-10): "))
                    if not 0 <= nota <= 10:
                        raise ValueError("La nota debe estar entre 0 y 10.")
                    notas_fase_general.append(nota)
                    break
                except ValueError:
                    print("Por favor, introduce un número válido entre 0 y 10.")

        nota_fase_general = sum(notas_fase_general) / 4

        notas_especificas = []
        for i in range(2):
            if input(f"¿Deseas introducir una asignatura específica {i+1}? (s/n): ").lower() == 's':
                while True:
                    try:
                        nota = float(input(f"Introduce la nota de la asignatura específica {i+1} (0-10): "))
                        if not 0 <= nota <= 10:
                            raise ValueError("La nota debe estar entre 0 y 10.")
                        ponderacion = float(input(f"Introduce la ponderación de la asignatura específica {i+1} (0.1 o 0.2): "))
                        if ponderacion not in (0.1, 0.2):
                           raise ValueError("La ponderación debe ser 0.1 o 0.2.")

                        notas_especificas.append((nota, ponderacion))
                        break
                    except ValueError:
                        print("Por favor, introduce un número válido para la nota (0-10) y la ponderación (0.1 o 0.2).")

        nota_acceso = 0.6 * media_bachillerato + 0.4 * nota_fase_general
        for nota, ponderacion in notas_especificas:
            nota_acceso += ponderacion * nota

        print(f"Nota de la fase general: {nota_fase_general:.2f}")
        print(f"Nota de acceso a la universidad: {nota_acceso:.3f}")

        nota_corte = float(input("Introduce la nota de corte para la carrera que te interesa: "))
        if nota_acceso >= nota_corte:
            print("¡Enhorabuena! Tu nota de acceso es suficiente para acceder a esta carrera.")
        else:
            print("Lo sentimos, tu nota de acceso no es suficiente para esta carrera.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

calcular_nota_acceso()