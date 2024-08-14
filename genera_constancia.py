from fpdf import FPDF
from PIL import Image

# Función para generar el PDF con una imagen de fondo y texto centrado
def generate_pdf(data, filename, background_image):
    # Crear un objeto FPDF con dimensiones personalizadas
    pdf = FPDF(unit='pt', format=[1650, 1275])
    pdf.add_page()
    
    # Cargar la imagen de fondo y ajustar el tamaño al tamaño de la página
    pdf.image(background_image, x=0, y=0, w=1650, h=1275)
    
    pdf.set_font("Arial", size=48)  # Tamaño de la fuente grande para adaptarse al tamaño del PDF
    
    # Variables para centrar el texto verticalmente y luego bajarlo 30 píxeles
    line_height = pdf.font_size * 2  # Altura de cada línea de texto
    total_text_height = line_height * len(data)  # Altura total del bloque de texto
    
    y_start = (1275 - total_text_height) / 2 + 30  # Posición inicial en el eje y para centrar y bajar el texto
    
    # Ajustar el texto sobre el fondo, centrado horizontal y verticalmente
    for value in data.values():
        text = str(value)  # Convertir el valor a cadena de texto
        text_width = pdf.get_string_width(text) + 6
        pdf.set_xy((1650 - text_width) / 2, y_start)
        pdf.cell(text_width, line_height, text, ln=True, align='C')
        y_start += line_height  # Mover la posición y para la siguiente línea de texto
    
    pdf.output(filename)
