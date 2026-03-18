import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Analítica Grupo 16 - Talento Tech",
    page_icon="📊",
    layout="wide"
)

# --- 2. FUNCIÓN DE CARGA DE DATOS (API JSON) ---
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    # Usamos el endpoint JSON de Socrata (más estable que el CSV)
    api_url = "https://www.datos.gov.co/resource/n48w-gutb.json?$limit=5000"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        
        # Estandarizar nombres de columnas (minúsculas y sin espacios)
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        
        # Limpieza básica de nulos
        if 'sector' in df.columns:
            df['sector'] = df['sector'].fillna('No Definido')
        if 'nombre_de_la_entidad' in df.columns:
            df['nombre_de_la_entidad'] = df['nombre_de_la_entidad'].fillna('Otra Entidad')
            
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- 3. ESTILOS CSS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: gray; font-size: 12px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LÓGICA DE NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- VISTA: INICIO (HOME) ---
if st.session_state.view == 'home':
    st.title("🚀 Sistema de Inteligencia de Datos")
    st.subheader("Proyecto Integrador - Grupo 16 | Talento Tech")
    
    col_img, col_txt = st.columns([2, 1])
    with col_img:
        st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", use_container_width=True)
    with col_txt:
        st.write("Bienvenido al panel de análisis de Datos Abiertos de Colombia.")
        st.write("Esta herramienta permite visualizar la distribución de información pública de manera interactiva.")
        if st.button("📊 Entrar al Dashboard", use_container_width=True, type="primary"):
            st.session_state.view = 'dashboard'
            st.rerun()

# --- VISTA: DASHBOARD ---
else:
    df = load_data()
    
    if df.empty:
        st.error("No se pudieron cargar los datos. Reintenta en unos minutos.")
        if st.button("🏠 Volver"):
            st.session_state.view = 'home'
            st.rerun()
    else:
        # --- BARRA LATERAL (FILTROS) ---
        st.sidebar.header("Filtros de Análisis")
        if st.sidebar.button("🏠 Inicio"):
            st.session_state.view = 'home'
            st.rerun()
        
        # Filtro dinámico por Sector
        sectores_unicos = sorted(df['sector'].unique())
        sector_selected = st.sidebar.multiselect("Selecciona Sectores:", sectores_unicos, default=sectores_unicos[:3])
        
        # Filtrar el DataFrame
        df_filtered = df[df['sector'].isin(sector_selected)]

        # --- CUERPO DEL DASHBOARD ---
        st.title("📊 Panel de Visualización")
        
        # Métricas principales
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Registros", len(df_filtered))
        m2.metric("Sectores Seleccionados", len(sector_selected))
        m3.metric("Entidades Únicas", df_filtered['nombre_de_la_entidad'].nunique() if 'nombre_de_la_entidad' in df_filtered.columns else 0)

        st.divider()

        # Gráficos
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### 🏢 Top 10 Entidades")
            if 'nombre_de_la_entidad' in df_filtered.columns:
                top_entidades = df_filtered['nombre_de_la_entidad'].value_counts().head(10).reset_index()
                fig_bar = px.bar(top_entidades, x='count', y='nombre_de_la_entidad', 
                                 orientation='h', color='count', color_continuous_scale='Blues')
                st.plotly_chart(fig_bar, use_container_width=True)

        with col_right:
            st.markdown("### 🍰 Distribución por Sector")
            fig_pie = px.pie(df_filtered, names='sector', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Tabla de datos
        with st.expander("👀 Ver tabla de datos filtrados"):
            st.dataframe(df_filtered, use_container_width=True)

st.markdown("<div class='footer'>© 2024 Grupo 16 - Talento Tech Colombia</div>", unsafe_allow_html=True)
