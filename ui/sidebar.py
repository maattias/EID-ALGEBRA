#ui/sidebar.py

"""
Módulo de navegación y parametrización de la interfaz gráfica.

Renderiza el panel lateral (Sidebar) permitiendo al usuario mutar las variables 
de estado global (K vecinos, usuario objetivo) que controlan el motor algebraico.
"""

import pandas as pd
import streamlit as st

from src.data_loader import (
    obtener_estadisticas,
    obtener_lista_usuarios,
    obtener_peliculas_usuario,
)


def render_sidebar(datos: dict) -> dict:
    """Renderiza los controles principales de la aplicacion."""
    df = datos["df"]
    matriz = datos["matriz"]

    with st.sidebar:
        st.markdown("## SistemaRec")
        st.caption("Filtrado colaborativo con similitud coseno")
        st.divider()
        st.markdown("#### Usuario objetivo")
        lista_usuarios = obtener_lista_usuarios(df)

        # El selector inyecta el valor automáticamente en la sesión local
        user_id = st.selectbox(
            label="Selecciona un usuario",
            options=lista_usuarios,
            index=0,
        )
        _mostrar_perfil_usuario(df, user_id)
        st.divider()
        
        st.markdown("#### Parametros de similitud")

        k_vecinos_similitud = st.slider(
            label="Usuarios similares a mostrar",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
        )

        st.divider()

        st.markdown("#### Visualizacion")

        # Limita de forma dinámica el máximo del slider según el tamaño real de la matriz
        max_heatmap = max(1, min(100, len(matriz)))
        valor_heatmap = min(30, max_heatmap)

        n_muestra_heatmap = st.slider(
            label="Usuarios en el heatmap",
            min_value=1,
            max_value=max_heatmap,
            value=valor_heatmap,
            step=1,
        )

        st.divider()

        _mostrar_info_dataset(df)

    return {                # dict: Variables paramétricas (user_id, k_vecinos_similitud, n_muestra_heatmap).
        "user_id": user_id,
        "k_vecinos_similitud": k_vecinos_similitud,
        "n_muestra_heatmap": n_muestra_heatmap,
    }


def _mostrar_perfil_usuario(df: pd.DataFrame, user_id: int) -> None:
    """Muestra un resumen compacto del usuario seleccionado."""
    peliculas_usuario = obtener_peliculas_usuario(df, user_id)
    n_valoradas = len(peliculas_usuario)

    if n_valoradas == 0:
        rating_promedio = 0.0
    else:
        rating_promedio = round(peliculas_usuario["rating"].mean(), 2)

    col1, col2 = st.columns(2)

    col1.metric("Peliculas valoradas", n_valoradas)
    col2.metric("Rating promedio", rating_promedio)


def _mostrar_info_dataset(df: pd.DataFrame) -> None:
    """Muestra estadisticas generales del dataset."""
    stats = obtener_estadisticas(df)

    st.markdown("#### Dataset")
    st.write(f"Usuarios: {stats['n_usuarios']:,}")
    st.write(f"Peliculas: {stats['n_peliculas']:,}")
    st.write(f"Valoraciones: {stats['n_valoraciones']:,}")
    st.write(f"Densidad de la matriz: {stats['densidad']}%")
    st.caption("MovieLens 100K")