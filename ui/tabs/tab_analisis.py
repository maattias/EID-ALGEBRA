
#ui/tabs/tab_analisis.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def _get_ratings_df():
    for key in ["ratings_df", "ratings", "dataset", "data"]:
        value = st.session_state.get(key)
        if isinstance(value, pd.DataFrame):
            return value
    return None


def _get_col(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def _recommendations_to_df():
    """
    Recupera recomendaciones guardadas en st.session_state.
    """

    fixed_keys = [
        "recommendation_history",
        "recommendations_history",
        "all_recommendations",
        "recommendations_df",
        "recommendations",
    ]

    frames = []

    for key in fixed_keys:
        value = st.session_state.get(key)

        if isinstance(value, pd.DataFrame) and not value.empty:
            frames.append(value)

        elif isinstance(value, list) and value:
            frames.append(pd.DataFrame(value))

    for key, value in st.session_state.items():
        if key.startswith("recs_"):
            if isinstance(value, pd.DataFrame) and not value.empty:
                frames.append(value)

            elif isinstance(value, list) and value:
                frames.append(pd.DataFrame(value))

    if not frames:
        return None

    return pd.concat(frames, ignore_index=True)

def _plot_rating_distribution(ratings_df, rating_col):
    fig, ax = plt.subplots(figsize=(8, 4))
    ratings_df[rating_col].value_counts().sort_index().plot(kind="bar", ax=ax)
    ax.set_title("Distribución general de ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Cantidad de valoraciones")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def _plot_top_recommended(recommendations_df):
    if recommendations_df is None or recommendations_df.empty:
        st.info("Aún no hay recomendaciones generadas. Este gráfico aparecerá cuando `src/recommender.py` guarde resultados en `st.session_state`.")
        return

    title_col = _get_col(
        recommendations_df,
        ["pelicula", "Película", "title", "movieTitle", "movie_title", "nombre"]
    )
    movie_col = _get_col(recommendations_df, ["movieId", "movie_id", "itemId", "item_id"])

    if title_col:
        labels = recommendations_df[title_col].dropna().astype(str).tolist()
    elif movie_col:
        labels = recommendations_df[movie_col].dropna().astype(str).tolist()
    else:
        st.warning("No se encontró una columna de película en las recomendaciones.")
        return

    counter = Counter(labels)
    top_items = pd.DataFrame(counter.most_common(10), columns=["Película", "Frecuencia"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_items["Película"][::-1], top_items["Frecuencia"][::-1])
    ax.set_title("Películas recomendadas con mayor frecuencia")
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel("Película")
    ax.grid(axis="x", alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_tab_analisis():
    st.header("Análisis experimental del sistema")

    ratings_df = _get_ratings_df()

    if ratings_df is None or ratings_df.empty:
        st.error("No hay dataset cargado en `st.session_state`.")
        return

    user_col = _get_col(ratings_df, ["userId", "user_id", "user"])
    movie_col = _get_col(ratings_df, ["movieId", "movie_id", "itemId", "item_id"])
    rating_col = _get_col(ratings_df, ["rating", "score", "valoracion"])

    if not user_col or not movie_col or not rating_col:
        st.error("El dataset debe tener columnas equivalentes a userId, movieId y rating.")
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Usuarios", ratings_df[user_col].nunique())

    with col2:
        st.metric("Películas", ratings_df[movie_col].nunique())

    with col3:
        st.metric("Valoraciones", len(ratings_df))

    st.subheader("Distribución general de ratings")
    _plot_rating_distribution(ratings_df, rating_col)

    st.subheader("Productos más recomendados")
    recommendations_df = _recommendations_to_df()
    _plot_top_recommended(recommendations_df)

    with st.expander("Vista previa del dataset"):
        st.dataframe(ratings_df.head(20), use_container_width=True)


render = render_tab_analisis