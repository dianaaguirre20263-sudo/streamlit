import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Analítica Grupo 16 - Talento Tech",
    page_icon="📊",
    layout="wide"
)

# --- 2. FUNCIÓN DE CARGA DE DATOS (API JSON) ---
@st.cache_data(ttl=3600)
def load_data():
    api_url = "https://www.datos.gov.co/resource/n48w-gutb.json?$limit=5000"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data_json = response.json()
        if not data_json: return pd.DataFrame()
        df = pd.DataFrame(data_json)
        df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- 3. LÓGICA DE IMAGEN (CORRECCIÓN GITHUB) ---
# Intentamos cargar la imagen desde el archivo local (si está en la misma carpeta de GitHub)
nombre_imagen = "internet-que-es-portada-890x445-1.jpg"

# --- 4. GESTIÓN DE VISTAS ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- VISTA: INICIO ---
if st.session_state.view == 'home':
    st.title("🚀 Sistema de Inteligencia de Datos")
    st.subheader("Proyecto Integrador - Grupo 16 | Talento Tech")
    
    # Lógica para mostrar imagen sin errores
    if os.path.exists(nombre_imagen):
        st.image(nombre_imagen, use_container_width=True, caption="Transformación Digital")
    else:
        # Si no la encuentra localmente, usa la URL de respaldo
        st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", 
                 use_container_width=True)
    
    if st.button("📊 Entrar al Dashboard", use_container_width=True, type="primary"):
        st.session_state.view = 'dashboard'
        st.rerun()

# --- VISTA: DASHBOARD ---
else:
    df = load_data()
    
    if df.empty:
        st.error("⚠️ No hay datos disponibles.")
        if st.button("🏠 Inicio"):
            st.session_state.view = 'home'
            st.rerun()
    else:
        # Identificar columnas automáticamente para evitar KeyError
        cols = df.columns.tolist()
        c_sector = 'sector' if 'sector' in cols else cols[0]
        c_entidad = 'nombre_de_la_entidad' if 'nombre_de_la_entidad' in cols else (cols[1] if len(cols)>1 else cols[0])

        st.sidebar.header("Panel de Control")
        if st.sidebar.button("🏠 Volver al Inicio"):
            st.session_state.view = 'home'
            st.rerun()

        # Filtro
        opciones = sorted(df[c_sector].dropna().unique().tolist())
        seleccion = st.sidebar.multiselect(f"Filtrar por {c_sector}:", opciones, default=opciones[:2])
        df_filtered = df[df[c_sector].isin(seleccion)]

        st.title("📊 Dashboard Interactivo")
        
        # Gráficos
        tab1, tab2 = st.tabs(["📈 Análisis Visual", "📋 Datos y Descarga"])

        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                fig_pie = px.pie(df_filtered, names=c_sector, title=f"Distribución {c_sector}", hole=0.3)
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_b:
                top_10 = df_filtered[c_entidad].value_counts().head(10).reset_index()
                fig_bar = px.bar(top_10, x='count', y=c_entidad, orientation='h', title="Top 10 Entidades")
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            st.write("### Tabla de Datos Filtrados")
            # Botón de descarga para el Grupo 16
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar datos como CSV",
                data=csv,
                file_name='datos_grupo16.csv',
                mime='text/csv',
            )
            st.dataframe(df_filtered, use_container_width=True)

st.markdown("<br><hr><center style='color:gray'>Grupo 16 - Talento Tech 2024</center>", unsafe_allow_html=True)
