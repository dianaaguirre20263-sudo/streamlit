import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Analítica Grupo 16 - Talento Tech",
    page_icon="📊",
    layout="wide"
)

# --- 2. FUNCIÓN DE CARGA DE DATOS (API JSON) ---
@st.cache_data(ttl=3600)
def load_data():
    # Endpoint JSON de Socrata
    api_url = "https://www.datos.gov.co/resource/n48w-gutb.json?$limit=5000"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data_json = response.json()
        
        if not data_json:
            return pd.DataFrame()
            
        df = pd.DataFrame(data_json)
        
        # Limpiamos nombres de columnas: minúsculas y sin espacios
        df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
        
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- 3. LÓGICA DE NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- VISTA: INICIO ---
if st.session_state.view == 'home':
    st.title("🚀 Sistema de Inteligencia de Datos")
    st.subheader("Proyecto Integrador - Grupo 16 | Talento Tech")
    
    st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", use_container_width=True)
    
    if st.button("📊 Entrar al Dashboard", use_container_width=True, type="primary"):
        st.session_state.view = 'dashboard'
        st.rerun()

# --- VISTA: DASHBOARD ---
else:
    df = load_data()
    
    if df.empty:
        st.error("⚠️ La API no devolvió datos. Es posible que el servicio esté en mantenimiento.")
        if st.button("🏠 Volver al Inicio"):
            st.session_state.view = 'home'
            st.rerun()
    else:
        # --- SOLUCIÓN AL KEYERROR ---
        # Verificamos qué columnas existen realmente en el dataset
        columnas_reales = df.columns.tolist()
        
        # Intentamos identificar la columna de 'sector' o una similar
        col_sector = 'sector' if 'sector' in columnas_reales else (columnas_reales[0] if columnas_reales else None)
        col_entidad = 'nombre_de_la_entidad' if 'nombre_de_la_entidad' in columnas_reales else (columnas_reales[1] if len(columnas_reales) > 1 else columnas_reales[0])

        st.sidebar.header("Panel de Control")
        if st.sidebar.button("🏠 Inicio"):
            st.session_state.view = 'home'
            st.rerun()

        # Filtro dinámico seguro
        st.sidebar.write(f"Filtrando por: **{col_sector.replace('_', ' ').title()}**")
        opciones = sorted(df[col_sector].dropna().unique().tolist())
        seleccion = st.sidebar.multiselect("Selecciona opciones:", opciones, default=opciones[:3])

        # Filtrado
        df_filtered = df[df[col_sector].isin(seleccion)]

        # --- VISUALIZACIÓN ---
        st.title("📊 Dashboard Interactivo")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Registros", len(df_filtered))
        col2.metric("Categorías", df_filtered[col_sector].nunique())
        col3.metric("Columnas", len(columnas_reales))

        st.divider()

        tab1, tab2 = st.tabs(["📈 Gráficos de Análisis", "📋 Explorador de Tabla"])

        with tab1:
            c_a, c_b = st.columns(2)
            
            with c_a:
                st.subheader(f"Distribución por {col_sector.title()}")
                fig_pie = px.pie(df_filtered, names=col_sector, hole=0.3, color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(fig_pie, use_container_width=True)

            with c_b:
                st.subheader(f"Top 10 por {col_entidad.replace('_', ' ').title()}")
                top_data = df_filtered[col_entidad].value_counts().head(10).reset_index()
                fig_bar = px.bar(top_data, x='count', y=col_entidad, orientation='h', color='count')
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            st.write("Datos actuales seleccionados:")
            st.dataframe(df_filtered, use_container_width=True)

st.markdown("<br><hr><center style='color:gray'>Grupo 16 - Talento Tech 2024</center>", unsafe_allow_html=True)
