"""
Autor: Matías

Controles disponibles:
    - Selector de usuario objetivo
    - Slider: número de recomendaciones (1–20)
    - Slider: número de vecinos a considerar (5–50)
    - Slider: tamaño de muestra para el heatmap (10–100)
    - Sección de información del dataset cargado
"""

import streamlit as st
import pandas as pd
from src.data_loader import obtener_lista_usuarios, obtener_estadisticas, obtener_peliculas_usuario


def render_sidebar(datos: dict) -> dict:
    """
    Renderiza el sidebar completo con todos los controles de la app.

    Parámetros
    ----------
    datos : dict
        Diccionario con claves 'df', 'matriz' y 'similitud'
        retornado por inicializar_datos() en app.py.

    Retorna
    -------
    dict con los parámetros seleccionados por el usuario:
        user_id             → int   — usuario objetivo seleccionado
        n_recomendaciones   → int   — cuántas películas recomendar
        k_vecinos           → int   — cuántos vecinos similares considerar
        n_muestra_heatmap   → int   — usuarios para el mapa de calor
    """
    df         = datos["df"]
    matriz     = datos["matriz"]
    similitud  = datos["similitud"]

    with st.sidebar:

        # ── Logo / título del sidebar ──────────────────────────────────────
        st.markdown("## 🎬 SistemaRec")
        st.caption("Filtrado colaborativo · similitud coseno")
        st.divider()

        # ── Selector de usuario ────────────────────────────────────────────
        st.markdown("#### 👤 Usuario objetivo")

        lista_usuarios = obtener_lista_usuarios(df)

        user_id = st.selectbox(
            label="Selecciona un usuario",
            options=lista_usuarios,
            index=0,
            help="El sistema generará recomendaciones personalizadas para este usuario.",
            label_visibility="collapsed",
        )

        # Mostrar mini-resumen del usuario seleccionado
        _mostrar_perfil_usuario(df=df, user_id=user_id)

        st.divider()

        # ── Parámetros de recomendación ────────────────────────────────────
        st.markdown("#### ⚙️ Parámetros")

        n_recomendaciones = st.slider(
            label="Nº de recomendaciones",
            min_value=1,
            max_value=20,
            value=10,
            step=1,
            help="Cuántas películas mostrar en el resultado final.",
        )

        k_vecinos = st.slider(
            label="Nº de vecinos (K)",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help=(
                "Cuántos usuarios similares considerar para generar las recomendaciones. "
                "Más vecinos = más datos pero puede diluir la similitud."
            ),
        )

        st.divider()

        # ── Parámetros de visualización ────────────────────────────────────
        st.markdown("#### 📊 Visualización")

        n_muestra_heatmap = st.slider(
            label="Usuarios en el heatmap",
            min_value=10,
            max_value=min(100, len(matriz)),
            value=30,
            step=10,
            help="Cuántos usuarios incluir en el mapa de calor de similitud.",
        )

        st.divider()

        # ── Info del dataset cargado ───────────────────────────────────────
        _mostrar_info_dataset(df=df)

    return {
        "user_id":           user_id,
        "n_recomendaciones": n_recomendaciones,
        "k_vecinos":         k_vecinos,
        "n_muestra_heatmap": n_muestra_heatmap,
    }


# ── Componentes internos del sidebar ──────────────────────────────────────────

def _mostrar_perfil_usuario(df: pd.DataFrame, user_id: int) -> None:
    """
    Muestra un resumen compacto del perfil del usuario seleccionado:
    cuántas películas ha valorado y su rating promedio.
    """
    peliculas_usuario = obtener_peliculas_usuario(df=df, user_id=user_id)
    n_valoradas  = len(peliculas_usuario)
    rating_prom  = round(peliculas_usuario["rating"].mean(), 2) if n_valoradas > 0 else 0.0

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Películas valoradas", value=n_valoradas)
    with col2:
        st.metric(label="Rating promedio", value=f"⭐ {rating_prom}")


def _mostrar_info_dataset(df: pd.DataFrame) -> None:
    """
    Muestra estadísticas básicas del dataset en el sidebar.
    """
    stats = obtener_estadisticas(df)

    st.markdown("#### 🗄️ Dataset")
    st.markdown(
        f"""
        <div style="font-size: 0.8rem; color: #A0AEC0; line-height: 1.8;">
            👥 <b>{stats['n_usuarios']:,}</b> usuarios<br>
            🎬 <b>{stats['n_peliculas']:,}</b> películas<br>
            ⭐ <b>{stats['n_valoraciones']:,}</b> valoraciones<br>
            📊 Densidad: <b>{stats['densidad']}%</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("MovieLens 100K · GroupLens Research")