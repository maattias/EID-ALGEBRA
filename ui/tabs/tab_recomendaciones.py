#ui/tabs/tab_recomendaciones.py

import streamlit as st
from src.data_loader import obtener_peliculas_usuario
from src.recommender import obtener_k_vecinos, recomendar_con_titulos


def render_tab_recomendaciones():
    """Muestra recomendaciones personalizadas para el usuario seleccionado."""
    datos = st.session_state["datos"]

    df = datos["df"]
    matriz = datos["matriz"]
    similitud = datos["similitud"]

    user_id = st.session_state["selected_user"]

    st.header("Recomendaciones personalizadas")
    st.write(
        "El sistema busca usuarios similares mediante similitud coseno y recomienda "
        "peliculas que el usuario objetivo aun no ha valorado."
    )

    col1, col2 = st.columns(2)

    with col1:
        k_vecinos = st.slider(
            "Cantidad de vecinos similares",
            min_value=1,
            max_value=30,
            value=5,
            step=1,
        )

    with col2:
        n_recomendaciones = st.slider(
            "Cantidad de recomendaciones",
            min_value=1,
            max_value=20,
            value=10,
            step=1,
        )

    peliculas_usuario = obtener_peliculas_usuario(df, user_id)

    total_vistas = len(peliculas_usuario)
    promedio_usuario = peliculas_usuario["rating"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Usuario objetivo", user_id)
    col2.metric("Peliculas valoradas", total_vistas)
    col3.metric("Rating promedio", f"{promedio_usuario:.2f}")

    st.divider()

    vecinos = obtener_k_vecinos(
        user_id=user_id,
        similitud=similitud,
        k_vecinos=k_vecinos,
    )

    st.subheader("Usuarios mas similares")

    if vecinos.empty:
        st.warning("No se encontraron usuarios similares para generar recomendaciones.")
        return

    vecinos_df = vecinos.reset_index()
    vecinos_df.columns = ["Usuario similar", "Similitud coseno"]
    vecinos_df["Similitud coseno"] = vecinos_df["Similitud coseno"].round(4)

    st.dataframe(
        vecinos_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Peliculas recomendadas")

    recomendaciones = recomendar_con_titulos(
        user_id=user_id,
        matriz=matriz,
        similitud=similitud,
        df=df,
        k_vecinos=k_vecinos,
        n_recomendaciones=n_recomendaciones,
    )

    if recomendaciones.empty:
        st.info(
            "No se pudieron generar recomendaciones. "
            "Prueba aumentando la cantidad de vecinos similares."
        )
    else:
        recomendaciones = recomendaciones.rename(
            columns={
                "movieId": "ID pelicula",
                "title": "Pelicula",
                "puntaje_predicho": "Puntaje predicho",
            }
        )

        st.dataframe(
            recomendaciones,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    with st.expander("Ver peliculas ya valoradas por el usuario"):
        historial = peliculas_usuario[["movieId", "title", "rating"]].copy()
        historial = historial.sort_values("rating", ascending=False)

        historial = historial.rename(
            columns={
                "movieId": "ID pelicula",
                "title": "Pelicula",
                "rating": "Rating",
            }
        )

        st.dataframe(
            historial,
            use_container_width=True,
            hide_index=True,
        )