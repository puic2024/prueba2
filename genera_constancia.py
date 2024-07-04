import streamlit as st
import pandas as pd
# Título de la aplicación
st.title("Cargar y Mostrar Archivo CSV")
# Descripción de la aplicación
st.write("""
Esta aplicación te permite cargar un archivo CSV y visualizar su contenido en forma de DataFrame.
""")
# Subir el archivo CSV
uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])
# Si se sube un archivo
if uploaded_file is not None:
   try:
       # Leer el archivo CSV
       df = pd.read_csv(uploaded_file)
       # Mostrar algunas estadísticas básicas del DataFrame
       st.write("## Estadísticas del DataFrame:")
       st.write(df.describe())
       # Mostrar el DataFrame
       st.write("## Contenido del DataFrame:")
       st.dataframe(df)
   except Exception as e:
       st.error(f"Error al leer el archivo CSV: {e}")
else:
   st.info("Por favor, sube un archivo CSV para continuar.")