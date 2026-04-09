import streamlit as st
import pandas as pd

URL = "https://docs.google.com/spreadsheets/d/1Kfg7kAnjcu9-ItBddQUzSKZVkGyHnW-DH7hHxyG5dxk/export?format=csv&gid=686525238"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(URL, dtype=str)
    df["SERIE"] = df["SERIE"].fillna("").str.strip()
    return df

df = cargar_datos()

st.title("🔧 FS CONTROL")

serie = st.text_input("Introduce número de serie")

if serie:
    serie = serie.strip()
    
    exacto = df[df["SERIE"] == serie]
    parcial = df[df["SERIE"].str.contains(serie, na=False, case=False)]
    
    if not exacto.empty:
        st.success("✅ Coincidencia exacta")
        
        for _, row in exacto.iterrows():
            st.markdown(f"""
            **Código:** {row['CODIGO']}  
            **Herramienta:** {row['HERRAMIENTA']}  
            **Modelo:** {row['MODELO']}
            """)
    
    elif not parcial.empty:
        st.warning("⚠️ Coincidencias aproximadas")
        st.dataframe(parcial[["CODIGO","HERRAMIENTA","MODELO"]])
    
    else:
        st.error("❌ No encontrado")
        st.info("Revisa el número o prueba con menos dígitos")
