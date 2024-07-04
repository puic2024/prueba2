import streamlit as st
import pandas as pd
# Título de la aplicación
st.title("Cargar y Mostrar Archivo de Excel")
# Subir el archivo de Excel
uploaded_file = st.file_uploader("Elige un archivo de Excel", type=["xlsx"])
# Si se sube un archivo
if uploaded_file is not None:
   # Leer el archivo de Excel
   df = pd.read_excel(uploaded_file)
   # Mostrar el DataFrame
   st.write("DataFrame del archivo de Excel:")
   st.dataframe(df)
else:
   st.write("Por favor, sube un archivo de Excel para continuar.")