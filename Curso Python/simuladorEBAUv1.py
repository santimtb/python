from colorama import init, Fore, Back, Style

# Inicializar colorama
init()

fase_general = ("Castellano: lengua y literatura", "Valenciano: lengua i literaura", "Lengua Extranjera", "Historia de España","Matemáticas")
notas_general = []
notas_especifica = []

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
    return notas

def calcula_nota_general():
    media_general = 0
    for asignatura, nota in notas_general:
        media_general += nota
    return media_general / len(notas_general)

def calcula_nota_especifica():
    media_especifica = 0
    for nota, ponderacion in notas_especifica:
        if nota >= 5:
            media_especifica += nota * ponderacion
    return media_especifica

print(Back.YELLOW + Fore.RED + "<<< Simulador de EBAU >>>" + Back.RESET + Fore.RESET)
#Obtenemos la nota media de Bachillerato
print(Back.MAGENTA + "Nota Media de Bachillerato >>>"+ Fore.MAGENTA + Back.RESET)
while True:
    try:
        media_bachillerato = pide_nota("Bachillerato")
        if media_bachillerato < 5:
            raise ValueError("La nota media de Bachillerato no puede ser inferior a 5.")
        break
    except ValueError as e:
        print(f"Error: {e}")
    
#Obtenemos las notas de las fases general y específica
print(Back.GREEN + Fore.BLUE + "Fase Obligatoria >>>" + Back.RESET + Fore.GREEN)
notas_general = notas_fase_general()
print(Back.CYAN + Fore.BLUE + "Fase Voluntaria >>>" + Back.RESET + Fore.CYAN)
notas_especifica=notas_fase_especifica()

#Mostramos los resultados
print(Back.RED + Fore.WHITE + "R E S U L T A D O >>>" + Back.RESET + Fore.CYAN)
nau = media_bachillerato * 0.6 + calcula_nota_general() * 0.4
if nau >= 5 and calcula_nota_general() >= 4:
    print(Back.WHITE + Fore.BLACK + "El resultado de la EBAU es", Back.GREEN + Fore.WHITE + Style.BRIGHT + " APTO " + Back.RESET)
    print(f"{Fore.GREEN} Tu Nota de Acceso a la Universidad (NAU) es: {Style.BRIGHT}{nau:.2f}")
    print(f"{Style.RESET_ALL}{Fore.GREEN} Tu Nota de Acceso a la Titulación (NAT) es: {Style.BRIGHT}{nau + calcula_nota_especifica():.3f}")
else:
    print(Style.RESET_ALL + Back.WHITE + Fore.BLACK + "El resultado de tu EBAU es",Back.RED + Fore.WHITE + Style.BRIGHT + " NO APTO " + Back.RESET)
    print(f"{Fore.LIGHTRED_EX} Tu Nota de Acceso a la Universidad (NAU) es: {Style.BRIGHT}{nau:.2f}")

#Mostramos el Resumen
print(Style.RESET_ALL + Back.YELLOW + "F A S E    G E N E R A L >>>" + Back.RESET + Fore.YELLOW)
for asignatura, nota in notas_general:
    print(f"{Style.RESET_ALL}{Fore.YELLOW} {asignatura}: {Style.BRIGHT}{nota}")
print(f"Media de la Fase General: {Style.BRIGHT}{calcula_nota_general():.2f}")
print(f"{Style.RESET_ALL}{Back.BLUE}NAU = Media de Bachillerato: {media_bachillerato:.2f} * 0.6 + Media de la Fase General: {calcula_nota_general():.2f} * 0.4 = {Style.BRIGHT}{nau:.2f}{Back.RESET}")
print(Style.RESET_ALL + Back.CYAN + "F A S E    E S P E C Í F I C A >>>" + Back.RESET + Fore.CYAN)
i=1
for nota, ponderacion in notas_especifica:
    if nota < 5:
        print(f"{Style.RESET_ALL}{Fore.CYAN} Optativa {i}: {nota} - Ponderación: {ponderacion} = {Style.BRIGHT}0")
    else:
        print(f"{Style.RESET_ALL}{Fore.CYAN} Optativa {i}: {nota} - Ponderación: {ponderacion} = {Style.BRIGHT}{nota*ponderacion:.2f}")
    i+=1
if nau >= 5:
    print(f"{Style.RESET_ALL}{Back.BLUE}NAT = {nau:.3f} + {calcula_nota_especifica():.3f} = {Style.BRIGHT}{nau + calcula_nota_especifica():.3f}")

