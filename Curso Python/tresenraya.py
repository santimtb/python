
# Función para imprimir el tablero
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)

# Función para verificar si hay un ganador
def verificar_victoria(tablero, jugador):
    # Verificar filas, columnas y diagonales
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] == jugador:  # Fila
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] == jugador:  # Columna
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:      # Diagonal principal
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:      # Diagonal inversa
        return True
    return False

# Función para verificar si hay empate
def verificar_empate(tablero):
    for fila in tablero:
        if "-" in fila:
            return False
    return True

# Función principal del juego
def juego_3_en_raya():
    # Inicializar el tablero
    tablero = [
        ["-", "-", "-"],
        ["-", "-", "-"],
        ["-", "-", "-"]
    ]
    
    jugador_actual = "X"
    
    while True:
        imprimir_tablero(tablero)
        
        # Solicitar al jugador que ingrese su movimiento
        fila = int(input(f"Jugador {jugador_actual}, ingresa la fila (0, 1, 2): "))
        columna = int(input(f"Jugador {jugador_actual}, ingresa la columna (0, 1, 2): "))
        
        # Validar el movimiento
        if tablero[fila][columna] != "-":
            print("Posición no válida, elige otra.")
            continue
        
        # Colocar la marca en el tablero
        tablero[fila][columna] = jugador_actual
        
        # Verificar si el jugador actual ha ganado
        if verificar_victoria(tablero, jugador_actual):
            imprimir_tablero(tablero)
            print(f"¡Jugador {jugador_actual} ha ganado!")
            break
        
        # Verificar si hay empate
        if verificar_empate(tablero):
            imprimir_tablero(tablero)
            print("¡Es un empate!")
            break
        
        # Cambiar de jugador
        jugador_actual = "O" if jugador_actual == "X" else "X"

# Ejecutar el juego
juego_3_en_raya()