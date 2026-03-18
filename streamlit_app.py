import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Data Analytics - Grupo 16",
    page_icon="📊",
    layout="wide"
)

# --- ESTILOS ---
st.markdown("""
    <style>
    .main-title { color: #0E4677; font-size: 40px; font-weight: bold; text-align: center; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background: #0E4677; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS (ESTRATEGIA DEFINITIVA) ---
@st.cache_data
def load_data():
    """
    Carga datos usando la API JSON de Socrata para evitar bloqueos 403.
    ID del dataset: n48w-gutb
    """
    # Usamos el endpoint JSON que es más amigable para APIs
    api_url = "https://www.datos.gov.co/resource/n48w-gutb.json?$limit=5000"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Convertir JSON a DataFrame
        df = pd.DataFrame(response.json())
        
        if df.empty:
            return pd.DataFrame()

        # Limpieza de nombres de columnas
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        
        # Normalizar nombres de columnas comunes si la API los devuelve distinto
        if 'sector' in df.columns:
            df['sector'] = df['sector'].fillna('No Definido')
            
        return df
    except Exception as e:
        st.error(f"Error de conexión con la API: {e}")
        return pd.DataFrame()

# --- LÓGICA DE NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- VISTA: INICIO ---
if st.session_state.view == 'home':
    st.markdown("<h1 class='main-title'>Sistema de Inteligencia de Datos Abiertos</h1>", unsafe_allow_html=True)
    st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", use_container_width=True)
    
    st.info("Este panel analiza datos gubernamentales en tiempo real para el Grupo 16.")
    
    if st.button("🚀 Explorar Datos Ahora", use_container_width=True):
        st.session_state.view = 'dashboard'
        st.rerun()

# --- VISTA: DASHBOARD ---
else:
    with st.spinner('Conectando con la base de datos oficial...'):
        data = load_data()

    if data.empty:
        st.error("❌ No se pudo saltar el bloqueo del servidor. Intenta recargar la página o verifica tu conexión a internet.")
        if st.button("🔄 Reintentar"):
            st.rerun()
    else:
        st.sidebar.title("Panel de Control")
        if st.sidebar.button("🏠 Volver al Inicio"):
            st.session_state.view = 'home'
            st.rerun()

        tab1, tab2 = st.tabs(["📊 Gráficos Interactivos", "📑 Datos Crudos"])

        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Sectores")
                if 'sector' in data.columns:
                    sector_data = data['sector'].value_counts().head(10)
                    fig_sector = px.pie(values=sector_data.values, names=sector_data.index, hole=0.4)
                    st.plotly_chart(fig_sector, use_container_width=True)
            
            with col2:
                st.subheader("Entidades con más reportes")
                entidad_col = 'nombre_de_la_entidad' if 'nombre_de_la_entidad' in data.columns else data.columns[0]
                top_entidades = data[entidad_col].value_counts().head(10)
                st.bar_chart(top_entidades)

        with tab2:
            st.dataframe(data, use_container_width=True)

st.markdown("<div class='footer'>Grupo 16 - Talento Tech 2024</div>", unsafe_allow_html=True)
