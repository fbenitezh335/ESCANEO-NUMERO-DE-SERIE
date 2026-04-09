import streamlit as st
import pandas as pd

# 🔗 TU GOOGLE SHEETS (CSV)
URL = "https://docs.google.com/spreadsheets/d/1Kfg7kAnjcu9-ItBddQUzSKZVkGyHnW-DH7hHxyG5dxk/export?format=csv&gid=0"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(URL, dtype=str)
    df["Nº SERIE"] = df["Nº SERIE"].fillna("").str.strip()
    return df

df = cargar_datos()

# 🎨 CONFIGURACIÓN APP
st.set_page_config(
    page_title="Buscador FS",
    layout="centered"
)

st.title("🔧 FS CONTROL")

st.markdown("Introduce número de serie:")

serie = st.text_input("", placeholder="Ej: 806000088")

if serie:
    serie = serie.strip()
    
    # 🔍 EXACTO
    exacto = df[df["Nº SERIE"] == serie]
    
    # 🔍 PARCIAL
    parcial = df[df["Nº SERIE"].str.contains(serie, na=False, case=False)]
    
    if not exacto.empty:
        st.success("✅ Coincidencia exacta")
        
        for _, row in exacto.iterrows():
            st.markdown(f"""
            ### 🧾 Resultado
            **Código:** {row['CODIGO']}  
            **Herramienta:** {row['HERRAMIENTA']}  
            **Modelo:** {row['MODELO']}
            """)
    
    elif not parcial.empty:
        st.warning("⚠️ Coincidencias aproximadas")
        
        for _, row in parcial.iterrows():
            st.markdown(f"""
            **Código:** {row['CODIGO']}  
            **Herramienta:** {row['HERRAMIENTA']}  
            **Modelo:** {row['MODELO']}
            ---
            """)
    
    else:
        st.error("❌ No encontrado")
        st.info("💡 Revisa el número o prueba con menos dígitos")

# 🔄 BOTÓN REFRESCAR
if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()
    st.rerun()