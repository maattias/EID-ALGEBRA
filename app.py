#app.py

"""
Orquestador principal del Sistema de Recomendación.

Inicializa la aplicación web mediante Streamlit, gestiona la caché de la 
memoria para evitar el recálculo matricial y ensambla los módulos visuales.
"""

import streamlit as st

from src.data_loader import cargar_dataset, construir_matriz_usuario_pelicula
from src.model.similarity import calcular_matriz_similitud
from ui.sidebar import render_sidebar
from ui.tabs.tab_analisis import render_tab_analisis
from ui.tabs.tab_matematicas import render_tab_matematicas
from ui.tabs.tab_recomendaciones import render_tab_recomendaciones
from ui.tabs.tab_similitud import render_tab_similitud

# ── Configuración general de la página ────────────────────────────────────────

st.set_page_config(
    page_title="SistemaRec - Recomendaciones con Algebra Lineal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inyectar estilos globales ──────────────────────────────────────────────────

from ui.styles import cargar_estilos
cargar_estilos()

# ── Encabezado principal ───────────────────────────────────────────────────────
st.title("Sistema de Recomendacion")
st.caption("Sistema basado en matriz usuario-pelicula y similitud coseno")
st.divider()

# ── Carga de datos con Caché ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False) # Inyecta el resultado en RAM para evitar recálculos en re-renders
def inicializar_datos():
    """
    Carga el dataset, construye la matriz usuario-pelicula y calcula similitudes.
    Almacena los resultados algebraicos masivos en la memoria caché para evitar 
    el re-cálculo costoso en cada interacción o click dentro de la UI.
    """
    df = cargar_dataset()
    matriz = construir_matriz_usuario_pelicula(df, columna_item="movieId")
    similitud = calcular_matriz_similitud(matriz)

    return {
        "df": df,
        "matriz": matriz,
        "similitud": similitud,
    }

# Control de flujo de inicialización con manejo de excepciones
try:
    with st.spinner("Cargando dataset y calculando similitudes..."):
        datos = inicializar_datos()

except FileNotFoundError as error:
    st.error(
        "No se pudo cargar el dataset. Revisa que existan los archivos "
        "`u.data`, `u.item` y `u.user` dentro de `data/ml-100k/`."
    )
    with st.expander("Detalle del error"):
        st.code(str(error))
    st.stop()

except Exception as error:
    st.error("Ocurrio un error al inicializar la aplicacion.")

    with st.expander("Detalle del error"):
        st.code(str(error))

    st.stop()

# ── Seteo de variables de estado local ─────────────────────────────────────────

# Guardamos las matrices en el session_state para que los sub-módulos visuales 
# de las pestañas las puedan leer sin importar los refrescos de pantalla
st.session_state["datos"] = datos
# Mapeo de parámetros del sidebar hacia variables accesibles por los tabs
st.session_state["ratings_df"] = datos["df"]
st.session_state["user_item_matrix"] = datos["matriz"]
st.session_state["similarity_matrix"] = datos["similitud"]

# ── Sidebar y Pestañas ─────────────────────────────────────────────────────────

parametros = render_sidebar(datos=datos)

st.session_state["selected_user"] = parametros["user_id"]
st.session_state["sample_size"] = parametros["n_muestra_heatmap"]
st.session_state["k_vecinos_similitud"] = parametros["k_vecinos_similitud"]

# ── Construcción de Pestañas de Navegación ─────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Analisis",
        "Matematicas",
        "Similitud",
        "Recomendaciones",
    ]
)

with tab1:
    render_tab_analisis()       # Renderiza los gráficos estadísticos del EDA
with tab2:
    render_tab_matematicas()    # Renderiza el simulador interactivo de 3x3
with tab3:
    render_tab_similitud()      # Renderiza el mapa de calor de correlaciones
with tab4:
    render_tab_recomendaciones() # Renderiza el recomendador filtrado por NaNs