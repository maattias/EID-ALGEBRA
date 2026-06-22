import streamlit as st

from src.data_loader import build_user_item_matrix, load_dataset
from src.model.similarity import calculate_similarity_matrix
from ui.sidebar import render_sidebar
from ui.styles import cargar_estilos
from ui.tabs.tab_analisis import render_tab_analisis
from ui.tabs.tab_matematicas import render_tab_matematicas
from ui.tabs.tab_recomendaciones import render_tab_recomendaciones
from ui.tabs.tab_similitud import render_tab_similitud


st.set_page_config(
    page_title="SistemaRec - Recomendaciones con Algebra Lineal",
    layout="wide",
    initial_sidebar_state="expanded",
)

cargar_estilos()

st.title("Sistema de Recomendacion")
st.caption("Sistema basado en matriz usuario-pelicula y similitud coseno")
st.divider()


@st.cache_data(show_spinner=False)
def inicializar_datos():
    """Carga el dataset, construye la matriz usuario-pelicula y calcula similitudes."""
    df = load_dataset()
    matriz = build_user_item_matrix(df, item_col="movieId")
    similitud = calculate_similarity_matrix(matriz)

    return {
        "df": df,
        "matriz": matriz,
        "similitud": similitud,
    }

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


st.session_state["datos"] = datos
st.session_state["ratings_df"] = datos["df"]
st.session_state["user_item_matrix"] = datos["matriz"]
st.session_state["similarity_matrix"] = datos["similitud"]

parametros = render_sidebar(datos=datos)

st.session_state["selected_user"] = parametros["user_id"]
st.session_state["sample_size"] = parametros["n_muestra_heatmap"]

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Analisis",
        "Matematicas",
        "Similitud",
        "Recomendaciones",
    ]
)

with tab1:
    render_tab_analisis()

with tab2:
    render_tab_matematicas()

with tab3:
    render_tab_similitud()

with tab4:
    render_tab_recomendaciones()