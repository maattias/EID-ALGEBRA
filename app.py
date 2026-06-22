import streamlit as st

from ui.sidebar import render_sidebar
#from ui.tabs.tab_recomendaciones import render_tab_recomendaciones
from ui.tabs.tab_analisis import render_tab_analisis
from ui.tabs.tab_similitud import render_tab_similitud

from src.data_loader import load_dataset, build_user_item_matrix
from src.model.similarity import calculate_similarity_matrix
from ui.styles import cargar_estilos


st.set_page_config(
    page_title="SistemaRec — Recomendaciones con Álgebra Lineal",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

cargar_estilos()

st.title("🎬 Sistema de Recomendación")
st.caption("Basado en similitud coseno y álgebra lineal · MATE1187")
st.divider()


@st.cache_data(show_spinner=False)
def inicializar_datos():
    df = load_dataset()

    matriz = build_user_item_matrix(df, item_col="title")
    similitud = calculate_similarity_matrix(matriz)

    return {
        "df": df,
        "matriz": matriz,
        "similitud": similitud,
    }


with st.spinner("Cargando dataset y calculando similitudes..."):
    try:
        datos = inicializar_datos()
        carga_exitosa = True
    except FileNotFoundError:
        datos = None
        carga_exitosa = False
        st.session_state["error"] = "No se encontró el dataset."
    except Exception as e:
        datos = None
        carga_exitosa = False
        st.session_state["error"] = str(e)


if not carga_exitosa:
    st.error(
        "⚠️ No se pudo cargar la app. "
        "Revisa que el dataset esté en `data/ml-100k/` y que existan `u.data`, `u.item` y `u.user`."
    )

    with st.expander("Ver detalle del error"):
        st.code(st.session_state.get("error", "Error desconocido"))

    st.stop()


st.session_state["datos"] = datos
st.session_state["ratings_df"] = datos["df"]
st.session_state["user_item_matrix"] = datos["matriz"]
st.session_state["similarity_matrix"] = datos["similitud"]

parametros = render_sidebar(datos=datos)

st.session_state["selected_user"] = parametros["user_id"]
st.session_state["sample_size"] = parametros["n_muestra_heatmap"]


tab1, tab2 = st.tabs([
    "📊 Análisis",
    "🔗 Similitud",
])

with tab1:
    render_tab_analisis()

with tab2:
    render_tab_similitud()