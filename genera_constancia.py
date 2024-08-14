import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import os
from PIL import Image

# Función para generar el PDF con una imagen de fondo y texto centrado
def generate_pdf(data, filename, background_image):
    # Crear un objeto FPDF con dimensiones personalizadas
    pdf = FPDF(unit='pt', format=[1650, 1275])
    pdf.add_page()
    
    # Cargar la imagen de fondo y ajustar el tamaño al tamaño de la página
    pdf.image(background_image, x=0, y=0, w=1650, h=1275)
    
    pdf.set_font("Arial", size=24)  # Reducir tamaño de la fuente a la mitad
    
    # Variables para centrar el texto verticalmente y luego bajarlo 30 píxeles
    line_height = pdf.font_size * 2  # Altura de cada línea de texto
    total_text_height = line_height * len(data)  # Altura total del bloque de texto
    
    #y_start = (1275 - total_text_height) / 2 + 70  # Posición inicial en el eje y para centrar y bajar el texto
    y_start = 400
    
    # Ajustar el texto sobre el fondo, centrado horizontal y verticalmente
    for value in data.values():
        text = str(value)  # Convertir el valor a cadena de texto
        text_width = pdf.get_string_width(text) + 6
        pdf.set_xy((1650 - text_width) / 2, y_start)
        pdf.cell(text_width, line_height, text, ln=True, align='C')
        y_start += line_height  # Mover la posición y para la siguiente línea de texto
    
    pdf.output(filename)

# Función para crear archivos ZIP
def create_zip(pdf_files, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for pdf_file in pdf_files:
            zipf.write(pdf_file, os.path.basename(pdf_file))

# Configuración de Streamlit
st.title("Generador de constancias PUIC")

# Mostrar imagen al principio
st.image("imagenes/escudo.jpg")

# Cargar archivo CSV
uploaded_file = st.file_uploader("Cargar CSV", type=["csv"])
background_image = st.file_uploader("Cargar imagen de fondo", type=["png"])

if uploaded_file is not None and background_image is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("DataFrame:")
    st.dataframe(df)

    if st.button("Generar PDFs"):
        # Guardar la imagen de fondo en un archivo temporal
        bg_image_path = "background_image.png"
        with open(bg_image_path, "wb") as f:
            f.write(background_image.read())
        
        pdf_files = []
        for index, row in df.iterrows():
            data = row.to_dict()
            pdf_filename = f"{data['nombre']}.pdf"  # Ajusta según el campo de nombre
            generate_pdf(data, pdf_filename, bg_image_path)
            pdf_files.append(pdf_filename)
        
        zip_filename = "pdf_files.zip"
        create_zip(pdf_files, zip_filename)
        
        with open(zip_filename, "rb") as f:
            bytes_data = f.read()
            st.download_button(
                label="Descargar ZIP",
                data=bytes_data,
                file_name=zip_filename,
                mime="application/zip"
            )
        
        # Limpiar archivos temporales
        for pdf_file in pdf_files:
            os.remove(pdf_file)
        os.remove(zip_filename)
        os.remove(bg_image_path)
