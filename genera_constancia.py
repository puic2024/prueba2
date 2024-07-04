import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import os

# Función para generar el PDF con imagen centrada y texto centrado
def generate_pdf(data, filename, image_path):
    pdf = FPDF()
    pdf.add_page()
    
    # Verificar que la imagen exista
    if os.path.exists(image_path):
        # Añadir imagen centrada
        image_width = 50  # Ancho deseado de la imagen
        image_height = 50  # Altura deseada de la imagen
        page_width = pdf.w - 2 * pdf.l_margin
        image_x = (page_width - image_width) / 2
        image_y = pdf.t_margin + 10
        pdf.image(image_path, x=image_x, y=image_y, w=image_width, h=image_height)
        
        # Ajustar la posición para el texto debajo de la imagen
        pdf.set_y(image_y + image_height + 10)
    else:
        return
    
    # Añadir texto centrado
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        text = f"{key}: {value}"
        text_width = pdf.get_string_width(text) + 6
        pdf.set_x((page_width - text_width) / 2)
        pdf.cell(text_width, 10, text, ln=True, align='C')
    
    pdf.output(filename)

# Función para crear archivos ZIP
def create_zip(pdf_files, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for pdf_file in pdf_files:
            zipf.write(pdf_file, os.path.basename(pdf_file))

# Configuración de Streamlit
st.title("CSV to PDF Converter")

# Mostrar la imagen al principio
image_path = "imagenes/escudo.jpg"  # Ruta de la imagen
if os.path.exists(image_path):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="{image_path}" alt="Escudo" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error(f"Image not found: {image_path}")

# Cargar archivo CSV
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("DataFrame:")
    st.dataframe(df)

    if st.button("Generate PDFs and Download ZIP"):
        pdf_files = []

        for index, row in df.iterrows():
            data = row.to_dict()
            pdf_filename = f"{data['nombre']}.pdf"  # Ajusta según el campo de nombre
            generate_pdf(data, pdf_filename, image_path)
            pdf_files.append(pdf_filename)
        
        zip_filename = "pdf_files.zip"
        create_zip(pdf_files, zip_filename)
        
        with open(zip_filename, "rb") as f:
            bytes_data = f.read()
            st.download_button(
                label="Download ZIP",
                data=bytes_data,
                file_name=zip_filename,
                mime="application/zip"
            )
        
        # Limpiar archivos temporales
        for pdf_file in pdf_files:
            os.remove(pdf_file)
        os.remove(zip_filename)
