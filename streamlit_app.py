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
# 📊 Análisis Exploratorio y Modelado de Datos de Conectividad Digital en Colombia

# --- El acceso a Internet es un factor fundamental para el desarrollo social, educativo y económico de un país. Sin embargo, la disponibilidad del servicio no es uniforme entre las distintas regiones, lo que genera brechas digitales que afectan la calidad de vida de la población.

# --- En Colombia, los servicios de Internet fijo presentan variaciones según el departamento, municipio, proveedor, tecnología utilizada y segmento de usuarios. Analizar estos patrones permite entender cómo se distribuye la conectividad en el territorio nacional y cómo ha evolucionado a lo largo del tiempo.

# --- **Alcance del proyecto---
El presente proyecto se enfoca específicamente en el análisis de la conectividad digital en los departamentos de **Antioquia** y **Risaralda**, permitiendo un estudio más detallado y contextualizado de estas regiones.

---

## 🎯 Objetivo del Proyecto

# --- Diseñar una base de datos que permita **almacenar, organizar y analizar** la información relacionada con los accesos a Internet fijo en Colombia, facilitando consultas sobre:

# ---  Distribución geográfica del servicio  
# ---  Evolución temporal del acceso  
# --- Participación de proveedores  
# --- Uso de tecnologías de conexión  
# --- Comportamiento de los distintos segmentos de usuarios  
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
        z-index: 100;
    }
    /* Margen inferior para que el footer no tape contenido */
    .main .block-container {
        padding-bottom: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA Y LIMPIEZA DE DATOS ---
@st.cache_data
def load_data():
    url = "https://www.datos.gov.co/api/v3/views/n48w-gutb/query.csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        df['sector'] = df['sector'].fillna('No Definido')
        return df
    except Exception as e:
        st.error(f"Error en la conexión: {e}")
        return pd.DataFrame()

# --- GESTIÓN DE ESTADO ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- VISTAS ---
if st.session_state.view == 'home':
    st.markdown("<h1 class='main-title'>Sistema de Inteligencia de Datos Abiertos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #5D6D7E;'>Talento Tech | Proyecto Integrador - Grupo 16</p>", unsafe_allow_html=True)
    
    col_img1, col_img2, col_img3 = st.columns([1, 5, 1])
    with col_img2:
        st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", 
                 caption="Transformación Digital - Colombia", use_container_width=True)
    
    st.markdown("### 📋 Sobre este Proyecto")
    st.write("Analizamos el impacto de los Datos Abiertos en Colombia para el Grupo 16 de Talento Tech.")
    
    if st.button("🚀 Ingresar al Panel de Análisis", use_container_width=True):
        st.session_state.view = 'dashboard'
        st.rerun()

else:
    data = load_data()
    
    st.sidebar.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg")
    if st.sidebar.button("🏠 Inicio"):
        st.session_state.view = 'home'
        st.rerun()

    tab_exec, tab_stats, tab_info = st.tabs(["📊 Dashboard", "🧠 Análisis Experto", "📖 Documentación"])

    with tab_exec:
        st.header("Dashboard Ejecutivo")
        c1, c2, c3 = st.columns(3)
        c1.metric("Registros", len(data))
        c2.metric("Sectores", data['sector'].nunique())
        c3.metric("Entidades", data['nombre_de_la_entidad'].nunique())

        sector_counts = data['sector'].value_counts().reset_index().head(10)
        sector_counts.columns = ['sector', 'count']
        fig = px.bar(sector_counts, x='count', y='sector', orientation='h', title="Top 10 Sectores")
        st.plotly_chart(fig, use_container_width=True)

    with tab_stats:
        st.header("Análisis con Seaborn")
        fig, ax = plt.subplots(figsize=(10, 6))
        top_ent = data['nombre_de_la_entidad'].value_counts().head(10)
        sns.barplot(x=top_ent.values, y=top_ent.index, palette="Blues_d", ax=ax)
        ax.set_title("Top 10 Entidades (Análisis Estadístico)")
        st.pyplot(fig)
        st.info("Este gráfico de Seaborn permite visualizar la concentración de reportes por entidad pública.")

    with tab_info:
        st.header("Documentación Grupo 16")
        st.write("Metodología: Limpieza con Pandas, Visualización con Seaborn y Plotly.")

st.markdown("<div class='footer'>Grupo 16 - Talento Tech 2024</div>", unsafe_allow_html=True)
