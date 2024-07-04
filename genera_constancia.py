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
        # Añadir imagen
        pdf.image(image_path, x=10, y=10, w=50)
        
        # Añadir texto centrado
        pdf.set_font("Arial", size=12)
        for key, value in data.items():
            text = f"{key}: {value}"
            text_width = pdf.get_string_width(text) + 6
            pdf.set_x((pdf.w - text_width) / 2)
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
    st.image(image_path, caption="Escudo", use_column_width=False)
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
