import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import os
import ast

# Función para generar el PDF con una imagen de fondo y texto parametrizado
def generate_pdf(data, filename, background_image, font_settings):
    pdf = FPDF(unit='pt', format=[1650, 1275])
    pdf.add_page()
    pdf.image(background_image, x=0, y=0, w=1650, h=1275)
    y_start = 470
    
    for key, value in data.items():
        if key in font_settings:
            text = str(value)
            font_size = font_settings[key]['tamaño']
            font_type = font_settings[key]['tipo_letra']
            font_color = font_settings[key].get('color', (0, 0, 0))  # Color negro por defecto
            
            pdf.set_font(font_type, size=font_size)
            pdf.set_text_color(*font_color)
            
            line_height = pdf.font_size * 1.5
            text_width = 1100  # Ancho fijo para el texto
            pdf.set_xy((1650 - text_width) / 2, y_start)
            
            # Contar el número de líneas que el texto ocupará
            lines = pdf.multi_cell(text_width, line_height, text, align='C', split_only=True)
            lines_count = len(lines)
            
            # Dibujar el texto con salto de línea automático
            pdf.set_xy((1650 - text_width) / 2, y_start)
            pdf.multi_cell(text_width, line_height, text, align='C')
            
            # Ajustar y_start dependiendo del número de líneas ocupadas
            y_start += line_height * lines_count
    
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
font_file = st.file_uploader("Cargar archivo de configuración de fuentes (txt)", type=["txt"])

if uploaded_file is not None and background_image is not None and font_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("DataFrame:")
    st.dataframe(df)

    # Leer y mostrar el contenido del archivo de configuración de fuentes
    font_file_content = font_file.read().decode('utf-8')
    st.write("Contenido del archivo de configuración de fuentes (txt):")
    st.code(font_file_content, language='python')
    
    font_settings = ast.literal_eval(font_file_content)
    
    if st.button("Generar PDFs"):
        bg_image_path = "background_image.png"
        with open(bg_image_path, "wb") as f:
            f.write(background_image.read())
        
        pdf_files = []
        for index, row in df.iterrows():
            data = row.to_dict()
            pdf_filename = f"{data['nombre']}.pdf"
            generate_pdf(data, pdf_filename, bg_image_path, font_settings)
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
