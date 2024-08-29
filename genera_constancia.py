import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import os
import ast
from pdf2image import convert_from_path

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
            pdf.set_font(font_type, size=font_size)
            text_width = pdf.get_string_width(text) + 6
            line_height = pdf.font_size * 1.5
            pdf.set_xy((1650 - text_width) / 2, y_start)
            pdf.cell(text_width, line_height, text, ln=True, align='C')
            y_start += line_height
    
    pdf.output(filename)

# Función para convertir el primer PDF en una imagen para previsualización
def preview_pdf_as_image(pdf_filename):
    images = convert_from_path(pdf_filename, first_page=0, last_page=1)
    return images[0] if images else None

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

    font_settings = ast.literal_eval(font_file.read().decode('utf-8'))
    
    if st.button("Generar y previsualizar PDF"):
        bg_image_path = "background_image.png"
        with open(bg_image_path, "wb") as f:
            f.write(background_image.read())
        
        # Generar PDF para el primer registro
        first_data = df.iloc[0].to_dict()
        first_pdf_filename = f"{first_data['nombre']}_preview.pdf"
        generate_pdf(first_data, first_pdf_filename, bg_image_path, font_settings)
        
        # Convertir el PDF a imagen para previsualización
        preview_image = preview_pdf_as_image(first_pdf_filename)
        
        if preview_image:
            st.image(preview_image, caption="Previsualización del primer PDF")
        
        # Guardar PDFs y mostrar opción de descarga
        if st.button("Descargar ZIP"):
            pdf_files = [first_pdf_filename]
            for index, row in df.iloc[1:].iterrows():  # Generar el resto de los PDFs
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
