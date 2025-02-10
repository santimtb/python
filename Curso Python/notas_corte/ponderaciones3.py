import json
import re
import pandas as pd
import camelot  # Importa la librería camelot

def extraer_ponderaciones(pdf_path):
    """
    Extrae las ponderaciones de un PDF y las guarda en un archivo JSON.

    Args:
        pdf_path (str): La ruta al archivo PDF.
    """

    try:
        # Leer el PDF y extraer las tablas de todas las páginas
        tables = camelot.read_pdf(pdf_path, pages='all')  # Lee todas las páginas

        # Crear un DataFrame vacío para combinar todas las tablas
        combined_df = pd.DataFrame()

        # Iterar sobre las tablas y combinarlas
        for table in tables:
            df = table.df
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        # Limpiar el DataFrame: eliminar filas y columnas vacías
        combined_df = combined_df.dropna(how='all')
        combined_df = combined_df.dropna(axis=1, how='all')

        # Obtener la lista de asignaturas (primera fila)
        asignaturas = combined_df.iloc[0, 1:].tolist()

        # Crear el diccionario de ponderaciones
        ponderaciones = {}

        # Iterar sobre las filas (empezando desde la segunda)
        for _, row in combined_df.iloc[1:].iterrows():
            titulo_universidad = row[0]

            # Separar titulación y universidades usando expresiones regulares
            match = re.match(r"(.*)\((.*)\)", titulo_universidad)
            if match:
                titulacion = match.group(1).strip()
                universidades = [u.strip() for u in match.group(2).split(",")]
            else:
                titulacion = titulo_universidad.strip()
                universidades = []

            ponderaciones[titulacion] = {
                "universities": universidades,
                "subjects": {}
            }

            # Iterar sobre las asignaturas y sus ponderaciones
            for i, asignatura in enumerate(asignaturas):
                ponderacion = row[i + 1]
                try:
                    ponderacion = float(str(ponderacion).replace(",", "."))  # Convertir a float
                except ValueError:
                    ponderacion = None  # Si no es un número, guardar como None
                if ponderacion is not None:  # Solo guardar si la ponderación no es None
                    ponderaciones[titulacion]["subjects"][asignatura] = ponderacion

        # Guardar el diccionario en un archivo JSON
        with open("ponderaciones.json", "w", encoding="utf-8") as f:
            json.dump(ponderaciones, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error al procesar el PDF: {e}")

# Ejemplo de uso
pdf_path = "assets/Ponderaciones_2025.pdf"  # Reemplaza con la ruta a tu archivo PDF
extraer_ponderaciones(pdf_path)