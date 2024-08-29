import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import os
import ast

# Función para generar el PDF con una imagen de fondo y texto parametrizado
def generate_pdf(data, filename, background_image, font_settings, y_start, line_height_multiplier):
    pdf = FPDF(unit='pt', format=[1650, 1275])
    pdf.add_page()
    pdf.image(background_image, x=0, y=0, w=1650, h=1275)
    
    for key, value in data.items():
        if key in font_settings:
            text = str(value)
            font_size = font_settings[key]['tamaño']
            font_type = font_settings[key]['tipo_letra']
            font_style = font_settings[key].get('estilo', '')  # Estilo normal por defecto
            font_color = font_settings[key].get('color', (0, 0, 0))  # Color negro por defecto
            
            pdf.set_font(font_type, font_style, size=font_size)
            pdf.set_text_color(*font_color)
            
            line_height = pdf.font_size * line_height_multiplier
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

# Input para que el usuario defina el valor inicial de y_start
y_start_user = st.number_input("Valor inicial para y_start:", min_value=0, value=460)

# Input para que el usuario defina el valor del interlineado
line_height_multiplier = st.number_input("Valor del interlineado (multiplicador):", min_value=0.5, value=1.3, step=0.1)

# Input de texto para la configuración de las fuentes
font_settings_input = st.text_area("Introduce la configuración de las fuentes (en formato de diccionario):", height=300, value="""
{
    "dirigido": {"tamaño": 30, "tipo_letra": "Arial", "estilo": "", "color": (0, 0, 0)},
    "nombre": {"tamaño": 30, "tipo_letra": "Arial", "estilo": "", "color": (0, 0, 0)},
    "por": {"tamaño": 30, "tipo_letra": "Arial", "estilo": "", "color": (0, 0, 0)},
    "actividad": {"tamaño": 30, "tipo_letra": "Arial", "estilo": "", "color": (0, 0, 0)},
    "eslogan": {"tamaño": 30, "tipo_letra": "Arial", "estilo": "", "color": (0, 0, 0)},
    "fecha": {"tamaño": 30, "tipo_letra": "Arial", "estilo": "", "color": (0, 0, 0)}
}
""")

if uploaded_file is not None and background_image is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("DataFrame:")
    st.dataframe(df)
    
    try:
        font_settings = ast.literal_eval(font_settings_input)
    except Exception as e:
        st.error(f"Error en la configuración de fuentes: {e}")
        font_settings = None
    
    if font_settings and st.button("Generar PDFs"):
        bg_image_path = "background_image.png"
        with open(bg_image_path, "wb") as f:
            f.write(background_image.read())
        
        pdf_files = []
        for index, row in df.iterrows():
            data = row.to_dict()
            pdf_filename = f"{data['nombre']}.pdf"
            generate_pdf(data, pdf_filename, bg_image_path, font_settings, y_start_user, line_height_multiplier)
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
