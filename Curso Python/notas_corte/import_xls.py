import pandas as pd
import re # Importar el módulo de expresiones regulares

def procesar_titulacion(titulacion):
    titulacion = str(titulacion)  # Convertir a string en caso de valores NaN
    match = re.search(r"\((.*?)\)", titulacion)  # Buscar texto dentro de paréntesis
    facultad = match.group(1) if match else "Desconocida"  # Extraer facultad si existe
    titulacion_limpia = re.sub(r"\s*\(.*?\)", "", titulacion)  # Eliminar todo lo dentro de paréntesis
    return titulacion_limpia.strip(), facultad  # Retornar titulación sin paréntesis y facultad

# Función para eliminar "(Estudi General)" de la columna 'Titulación'
def limpiar_titulacion(titulacion):
    return re.sub(r"\s*\(Estudi General\)", "", str(titulacion))  # Reemplaza (Estudi General) con una cadena vacía

# Cargar las hojas del archivo Excel en diccionarios de DataFrames
hojas = pd.read_excel("assets/Notas de Corte 2024-25.xlsx", sheet_name=["UV", "UPV"])

# Lista para almacenar los datos con el nombre de la hoja
data = []

# Iterar sobre cada hoja y agregar el campo 'Fuente'
for nombre_hoja, df in hojas.items():
    # Limpiar la columna 'Titulación'
    df["Titulación"] = df["Titulación"].apply(limpiar_titulacion)
    #Agregamos el campos Universidad y Facultad
    df["Universidad"] = nombre_hoja  # Agregar columna con el nombre de la hoja
    # Aplicar la función y dividir en dos columnas
    df["Titulación"], df["Facultad"] = zip(*df["Titulación"].apply(procesar_titulacion))
    # Limpiar caracteres de escape en cada celda de texto
    df = df.applymap(lambda x: x.replace("\n", " ").replace("\t", " ").replace("\r", " ") if isinstance(x, str) else x)

    # Convertir cada fila en diccionario y añadir a la lista
    data.extend(df.to_dict(orient="records"))

# Convertir a JSON
json_data = pd.DataFrame(data).to_json(orient="records", indent=4)

# Guardar en un archivo JSON
with open("archivo.json", "w", encoding="utf-8") as f:
    f.write(json_data)

print("Archivo Excel convertido a JSON sin caracteres de escape.")
