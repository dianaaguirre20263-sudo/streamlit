import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Data Analytics - Grupo 16",
    page_icon="📊",
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; }
    .main-title { 
        color: #0E4677; 
        font-size: 42px; 
        font-weight: bold; 
        text-align: center;
        padding: 20px;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E4677;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA Y LIMPIEZA DE DATOS ---
@st.cache_data
def load_data():
    # Dataset de datos.gov.co: Usos de Datos Abiertos
    url = "https://www.datos.gov.co/api/v3/views/n48w-gutb/query.csv"
    try:
        df = pd.read_csv(url)
        # Normalización de columnas
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        # Imputación de nulos básica
        df['sector'] = df['sector'].fillna('No Definido')
        return df
    except Exception as e:
        st.error(f"Error en la conexión: {e}")
        return pd.DataFrame()

# --- GESTIÓN DE ESTADO (NAVEGACIÓN) ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

def change_view(target):
    st.session_state.view = target

# --- RENDERIZADO DE VISTAS ---

if st.session_state.view == 'home':
    # --- LANDING PAGE ---
    st.markdown("<h1 class='main-title'>Sistema de Inteligencia de Datos Abiertos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #5D6D7E;'>Talento Tech | Proyecto Integrador - Grupo 16</p>", unsafe_allow_html=True)
    
    col_img1, col_img2, col_img3 = st.columns([1, 5, 1])
    with col_img2:
        # Imagen técnica representativa
        st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", 
                 caption="Interconectividad y Flujo de Datos en el Estado Colombiano",
                 use_container_width=True)
    
    st.markdown("### 📋 Sobre este Proyecto")
    st.write("""
    Esta herramienta ha sido diseñada para analizar cómo las entidades públicas y la ciudadanía interactúan con los 
    **Datos Abiertos en Colombia**. A través de este panel, transformamos filas de información cruda en conocimiento 
    estratégico para el **Grupo 16**.
    """)
    
    if st.button("🚀 Ingresar al Panel de Análisis", use_container_width=True):
        st.session_state.view = 'dashboard'
        st.rerun()

else:
    # --- PANEL DE TRABAJO (DASHBOARD) ---
    data = load_data()

    # Sidebar con imagen y créditos
    st.sidebar.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg")
    st.sidebar.title("Configuración")
    
    if st.sidebar.button("🏠 Regresar al Inicio"):
        st.session_state.view = 'home'
        st.rerun()

    # Pestañas del Panel
    tab_exec, tab_stats, tab_info = st.tabs(["📊 Dashboard Ejecutivo", "🧠 Análisis Experto", "📖 Documentación"])

    with tab_exec:
        st.header("Resumen General de Actividad")
        
        # KPIs
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Casos de Uso", len(data))
        c2.metric("Sectores Líderes", data['sector'].nunique())
        c3.metric("Entidades Activas", data['nombre_de_la_entidad'].nunique())

        # Gráfico Interactivo Plotly
        sector_data = data['sector'].value_counts().reset_index().head(15)
        fig_plotly = px.bar(sector_data, x='count', y='sector', 
                            title="Top 15 Sectores por Volumen de Datos",
                            labels={'count':'N° de Usos', 'sector':'Sector'},
                            color='count', color_continuous_scale='Blues')
        st.plotly_chart(fig_plotly, use_container_width=True)

    with tab_stats:
        st.header("Análisis Estadístico Avanzado (Seaborn)")
        st.write("Exploración profunda de la distribución y tipología de los datos.")

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Distribución de Entidades")
            fig_sns1, ax_sns1 = plt.subplots(figsize=(8, 6))
            sns.set_palette("viridis")
            # Filtrar top 10 para claridad visual
            top_entidades = data['nombre_de_la_entidad'].value_counts().head(10)
            sns.barplot(x=top_entidades.values, y=top_entidades.index, ax=ax_sns1)
            ax_sns1.set_title("Top 10 Entidades Reportantes")
            st.pyplot(fig_sns1)
            st.info("**Explicación:** Este gráfico de barras horizontal permite identificar qué instituciones están centralizando el uso de datos abiertos actualmente.")

        with col_b:
            st.subheader("Frecuencia de Actualización")
            if 'frecuencia_de_actualizaci_n' in data.columns:
                fig_sns2, ax_sns2 = plt.subplots(figsize=(8, 6))
                sns.countplot(data=data, y='frecuencia_de_actualizaci_n', 
                              order=data['frecuencia_de_actualizaci_n'].value_counts().index[:10],
                              palette="magma", ax=ax_sns2)
                ax_sns2.set_title("Frecuencia de Mantenimiento de Datos")
                st.pyplot(fig_sns2)
                st.info("**Explicación:** La frecuencia de actualización es un indicador de la calidad y vigencia de la información disponible.")
            else:
                st.warning("Columna de frecuencia no disponible en este dataset.")

    with tab_info:
        st.header("Ficha Técnica y Metodología")
        st.markdown(f"""
        - **Grupo:** 16 (Talento Tech)
        - **Fuente:** [Portal Datos Abiertos Colombia](https://www.datos.gov.co)
        - **Dataset ID:** `n48w-gutb`
        - **Herramientas Utilizadas:** Streamlit, Pandas, Seaborn, Plotly.
        
        **Metodología de Análisis:**
        1. Limpieza de nombres de variables (lowercase & underscores).
        2. Análisis de frecuencias simples para identificación de sectores.
        3. Visualización comparativa para detectar brechas de uso.
        """)
        st.success("Análisis completado satisfactoriamente para el nivel Integrador.")

# Footer
st.markdown("<div class='footer'>Desarrollado por el Grupo 16 - Talento Tech 2024</div>", unsafe_allow_html=True)
