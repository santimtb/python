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
        # Leer el PDF y extraer las tablas
        tables = camelot.read_pdf(pdf_path, pages='1-2')  # Lee las páginas 1 y 2

        # Como camelot puede detectar varias tablas, elegimos la que contiene la información
        # Esto puede variar dependiendo del PDF, ajusta el índice si es necesario
        df = tables[0].df  

        # Limpiar el DataFrame: eliminar filas y columnas vacías
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')

        # Obtener la lista de asignaturas (primera fila)
        asignaturas = df.iloc[0, 1:].tolist()

        # Crear el diccionario de ponderaciones
        ponderaciones = {}

        # Iterar sobre las filas (empezando desde la segunda)
        for _, row in df.iloc[1:].iterrows():
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