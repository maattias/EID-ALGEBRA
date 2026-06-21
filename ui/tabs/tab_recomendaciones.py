"""

Contenido:
    - Encabezado con resumen del usuario seleccionado
    - Botón para generar recomendaciones
    - Lista de películas recomendadas con score y ranking
    - Tabla de películas ya vistas por el usuario (contexto)
"""

import streamlit as st
import pandas as pd
from src.recommender import recomendar
from src.data_loader import obtener_peliculas_usuario
from ui.components import (
    tarjeta_pelicula,
    separador_seccion,
    metrica_destacada,
    mensaje_vacio,
)


def render_tab_recomendaciones(datos: dict, parametros: dict) -> None:
    """
    Renderiza el tab de recomendaciones personalizadas.

    Parámetros
    ----------
    datos      : dict — claves 'df', 'matriz', 'similitud'
    parametros : dict — claves 'user_id', 'n_recomendaciones', 'k_vecinos'
    """
    df               = datos["df"]
    matriz           = datos["matriz"]
    similitud        = datos["similitud"]
    user_id          = parametros["user_id"]
    n_recomendaciones = parametros["n_recomendaciones"]
    k_vecinos        = parametros["k_vecinos"]

    # ── Encabezado ─────────────────────────────────────────────────────────
    separador_seccion(
        titulo=f"🎯 Recomendaciones para el Usuario {user_id}",
        descripcion=(
            f"Basadas en los {k_vecinos} usuarios más similares · "
            f"Mostrando top {n_recomendaciones} películas"
        ),
    )

    # ── Métricas del usuario ────────────────────────────────────────────────
    peliculas_vistas = obtener_peliculas_usuario(df=df, user_id=user_id)
    n_vistas    = len(peliculas_vistas)
    rating_prom = round(peliculas_vistas["rating"].mean(), 2) if n_vistas > 0 else 0.0

    col1, col2, col3 = st.columns(3)
    metrica_destacada(valor=str(user_id),         etiqueta="Usuario objetivo", col=col1)
    metrica_destacada(valor=f"{n_vistas}",        etiqueta="Películas valoradas", col=col2)
    metrica_destacada(valor=f"⭐ {rating_prom}",  etiqueta="Rating promedio", col=col3)

    st.divider()

    # ── Generación de recomendaciones ──────────────────────────────────────
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        generar = st.button("🔍 Generar recomendaciones", use_container_width=True)

    # Guardar resultado en session_state para no recalcular al mover sliders
    clave_cache = f"recs_{user_id}_{n_recomendaciones}_{k_vecinos}"

    if generar or clave_cache in st.session_state:

        if generar or clave_cache not in st.session_state:
            with st.spinner("Calculando recomendaciones..."):
                try:
                    resultado = recomendar(
                        user_id=user_id,
                        matriz=matriz,
                        matriz_similitud=similitud,
                        n_recomendaciones=n_recomendaciones,
                        k_vecinos=k_vecinos,
                    )
                    st.session_state[clave_cache] = resultado
                except Exception as e:
                    st.error(f"Error al generar recomendaciones: {e}")
                    return

        resultado = st.session_state[clave_cache]

        # ── Resultados ──────────────────────────────────────────────────────
        st.markdown(f"#### 🎬 Top {len(resultado)} películas recomendadas")

        if resultado.empty:
            mensaje_vacio(
                "No se encontraron recomendaciones para este usuario.",
                "Prueba aumentando el número de vecinos K en el sidebar.",
            )
        else:
            col_lista, col_detalle = st.columns([3, 2])

            with col_lista:
                for i, fila in resultado.iterrows():
                    tarjeta_pelicula(
                        titulo=fila["pelicula"],
                        score=fila["score_predicho"],
                        n_vecinos=fila["n_vecinos_que_valoraron"],
                        posicion=i + 1,
                    )

            with col_detalle:
                st.markdown("##### 📋 Tabla completa")
                st.dataframe(
                    resultado.rename(columns={
                        "pelicula":               "Película",
                        "score_predicho":         "Score",
                        "n_vecinos_que_valoraron": "Vecinos",
                    }),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Score": st.column_config.ProgressColumn(
                            "Score predicho",
                            format="%.2f",
                            min_value=0.0,
                            max_value=5.0,
                        ),
                    },
                )

        st.divider()

    # ── Historial del usuario ───────────────────────────────────────────────
    with st.expander(f"📖 Ver historial de valoraciones del Usuario {user_id}"):
        if peliculas_vistas.empty:
            mensaje_vacio("Este usuario no tiene valoraciones registradas.")
        else:
            columna_titulo = "title" if "title" in peliculas_vistas.columns else "movieId"
            st.dataframe(
                peliculas_vistas.rename(columns={
                    columna_titulo: "Película",
                    "rating":       "Rating",
                }),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rating": st.column_config.ProgressColumn(
                        "Rating",
                        format="%.1f ⭐",
                        min_value=0.0,
                        max_value=5.0,
                    ),
                },
            )