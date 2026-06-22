#ui/tabs/tab_analisis.py

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from src.data_loader import obtener_estadisticas


def _obtener_dataset():
    """Obtiene el dataset cargado desde session_state."""
    df = st.session_state.get("ratings_df")

    if isinstance(df, pd.DataFrame) and not df.empty:
        return df

    datos = st.session_state.get("datos")

    if isinstance(datos, dict):
        df = datos.get("df")

        if isinstance(df, pd.DataFrame) and not df.empty:
            return df

    return None


def _graficar_distribucion_ratings(df):
    """Grafica la distribucion general de calificaciones."""
    conteo = df["rating"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    conteo.plot(kind="bar", ax=ax)

    ax.set_title("Distribucion general de ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Cantidad de valoraciones")
    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)


def _graficar_peliculas_mas_valoradas(df):
    """Grafica las peliculas con mayor cantidad de valoraciones."""
    top = (
        df.groupby("title")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    top.plot(kind="barh", ax=ax)

    ax.set_title("Peliculas con mas valoraciones")
    ax.set_xlabel("Cantidad de valoraciones")
    ax.set_ylabel("Pelicula")
    ax.grid(axis="x", alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)


def _mostrar_mejores_promedios(df):
    """Muestra peliculas con mejor promedio considerando un minimo de valoraciones."""
    resumen = (
        df.groupby("title")
        .agg(
            promedio_rating=("rating", "mean"),
            cantidad_valoraciones=("rating", "count"),
        )
        .reset_index()
    )

    resumen = resumen[resumen["cantidad_valoraciones"] >= 50]
    resumen = resumen.sort_values("promedio_rating", ascending=False).head(10)

    resumen["promedio_rating"] = resumen["promedio_rating"].round(2)

    resumen = resumen.rename(
        columns={
            "title": "Pelicula",
            "promedio_rating": "Rating promedio",
            "cantidad_valoraciones": "Valoraciones",
        }
    )

    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True,
    )


def render_tab_analisis():
    """Muestra estadisticas exploratorias del dataset."""
    df = _obtener_dataset()

    if df is None:
        st.error("No hay dataset cargado.")
        return

    stats = obtener_estadisticas(df)

    st.header("Analisis del dataset")

    st.write(
        "Esta seccion resume el conjunto de datos MovieLens 100K usado para construir "
        "la matriz usuario-pelicula."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Usuarios", stats["n_usuarios"])
    col2.metric("Peliculas", stats["n_peliculas"])
    col3.metric("Valoraciones", stats["n_valoraciones"])
    col4.metric("Densidad", f"{stats['densidad']}%")

    st.divider()

    st.subheader("Distribucion de ratings")
    _graficar_distribucion_ratings(df)

    st.subheader("Peliculas con mas valoraciones")
    _graficar_peliculas_mas_valoradas(df)

    st.subheader("Peliculas mejor evaluadas")
    st.write(
        "Se consideran solo peliculas con al menos 50 valoraciones para evitar "
        "promedios poco representativos."
    )
    _mostrar_mejores_promedios(df)

    with st.expander("Vista previa del dataset"):
        columnas = [
            "userId",
            "movieId",
            "title",
            "rating",
            "age",
            "gender",
            "occupation",
        ]

        columnas_disponibles = [
            columna for columna in columnas
            if columna in df.columns
        ]

        st.dataframe(
            df[columnas_disponibles].head(20),
            use_container_width=True,
            hide_index=True,
        )