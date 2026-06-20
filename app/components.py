# app/components.py

import streamlit as st
import pandas as pd


def movie_card(title: str, genre: str, score: float):
    """
    Muestra una tarjeta con información de una película recomendada.

    Parámetros:
    ----------
    title : str
        Nombre de la película.
    genre : str
        Género principal.
    score : float
        Puntaje predicho por el recomendador.
    """

    st.markdown(
        f"""
        <div style="
            border:1px solid #d3d3d3;
            border-radius:10px;
            padding:15px;
            margin-bottom:10px;
        ">
            <h4>🎬 {title}</h4>
            <p><strong>Género:</strong> {genre}</p>
            <p><strong>⭐ Puntaje:</strong> {score:.3f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def similarity_table(sim_matrix):
    """
    Muestra una matriz de similitud entre usuarios.

    Parámetros:
    ----------
    sim_matrix : pd.DataFrame o np.ndarray
        Matriz de similitud calculada.
    """

    st.subheader("📊 Matriz de Similitud")

    if not isinstance(sim_matrix, pd.DataFrame):
        sim_matrix = pd.DataFrame(sim_matrix)

    st.dataframe(
        sim_matrix,
        use_container_width=True
    )


def user_profile_section(
    user_id,
    rated_movies,
    genres
):
    """
    Muestra información del usuario seleccionado.

    Parámetros:
    ----------
    user_id : int o str
        Usuario actual.

    rated_movies : list
        Lista de películas valoradas.

    genres : list
        Lista de géneros favoritos.
    """

    st.subheader("👤 Mi Perfil")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Usuario",
            user_id
        )

    with col2:
        st.metric(
            "Películas valoradas",
            len(rated_movies)
        )

    st.markdown("---")

    st.write("### 🎞️ Películas valoradas")

    if rated_movies:

        for movie in rated_movies:
            st.write(f"• {movie}")

    else:
        st.info(
            "Este usuario no tiene películas valoradas."
        )

    st.markdown("---")

    st.write("### 🎭 Géneros favoritos")

    if genres:

        for genre in genres:
            st.write(f"• {genre}")

    else:
        st.info(
            "No se han seleccionado géneros favoritos."
        )