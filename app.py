import streamlit as st
from ui.sidebar import render_sidebar
from ui.tabs.tab_recomendaciones import render_tab_recomendaciones
from ui.tabs.tab_analisis import render_tab_analisis
from ui.tabs.tab_similitud import render_tab_similitud
from ui.tabs.tab_matematicas import render_tab_matematicas
from src.data_loader import cargar_datos, construir_matriz
from src.similarity import calcular_matriz_similitud

# ── Configuración general de la página ────────────────────────────────────────

st.set_page_config(
    page_title="SistemaRec — Recomendaciones con Álgebra Lineal",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inyectar estilos globales ──────────────────────────────────────────────────

from ui.styles import cargar_estilos
cargar_estilos()

# ── Encabezado principal ───────────────────────────────────────────────────────

st.title("🎬 Sistema de Recomendación")
st.caption("Basado en similitud coseno y álgebra lineal · MATE1187")

st.divider()

# ── Carga de datos (con caché para no recalcular en cada interacción) ──────────

@st.cache_data(show_spinner=False)
def inicializar_datos():
    """
    Carga el dataset, construye la matriz usuario-producto
    y calcula la matriz de similitud completa.
    Retorna un diccionario con todo lo necesario para los tabs.
    """
    df = cargar_datos()
    matriz = construir_matriz(df)
    similitud = calcular_matriz_similitud(matriz)
    return {
        "df": df,
        "matriz": matriz,
        "similitud": similitud,
    }

# Indicador de carga visible al usuario
with st.spinner("Cargando dataset y calculando similitudes..."):
    try:
        datos = inicializar_datos()
        st.session_state["datos"] = datos
        carga_exitosa = True
    except FileNotFoundError:
        carga_exitosa = False
    except Exception as e:
        carga_exitosa = False
        st.session_state["error"] = str(e)

# Manejo de errores de carga
if not carga_exitosa:
    st.error(
        "⚠️ No se encontró el dataset. "
        "Revisa `data/INSTRUCCIONES_DATASET.md` para saber cómo descargarlo y dónde ubicarlo."
    )
    st.stop()

# ── Sidebar ────────────────────────────────────────────────────────────────────

parametros = render_sidebar(datos=st.session_state["datos"])

# ── Tabs principales ───────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Recomendaciones",
    "📊 Análisis",
    "🔗 Similitud",
    "📐 Matemáticas",
])

with tab1:
    render_tab_recomendaciones(
        datos=st.session_state["datos"],
        parametros=parametros,
    )

with tab2:
    render_tab_analisis(
        datos=st.session_state["datos"],
        parametros=parametros,
    )

with tab3:
    render_tab_similitud(
        datos=st.session_state["datos"],
        parametros=parametros,
    )

with tab4:
    render_tab_matematicas()