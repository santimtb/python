import fitz  # PyMuPDF
import json

# Abre el archivo PDF
pdf_document = "assets/Ponderaciones_2025.pdf"
pdf = fitz.open(pdf_document)

# Extrae el texto de cada página
text = ""
for page_num in range(len(pdf)):
    page = pdf.load_page(page_num)
    text += page.get_text()

# Divide el texto en líneas
lines = text.split('\n')

# Inicializa un diccionario vacío para almacenar los datos estructurados
data = {}

# Procesa las líneas para extraer la información
current_degree = None
for line in lines:
    if line.strip() == "":
        continue

    # Verifica si la línea contiene el nombre de una titulación
    if '(' in line and ')' in line:
        degree_info = line.strip()
        degree_name, universities = degree_info.rsplit('(', 1)
        degree_name = degree_name.strip()
        universities = universities.rstrip(')').strip()
        current_degree = degree_name
        data[current_degree] = {"universities": universities, "subjects": {}}
    elif current_degree:
        # Divide la línea en asignatura y ponderación
        parts = line.split()
        if len(parts) > 1 and parts[-1].replace(',', '').replace('.', '').isdigit():
            subject = " ".join(parts[:-1]).strip()
            weight = parts[-1].strip()
            data[current_degree]["subjects"][subject] = weight

# Convierte el diccionario a una cadena JSON
json_data = json.dumps(data, indent=4, ensure_ascii=False)

# Guarda la cadena JSON en un archivo
with open("Ponderaciones_2025.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)

print("La información se ha convertido y guardado en el archivo Ponderaciones_2025.json.")