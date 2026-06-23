# ui/tabs/tab_analisis.py

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.data_loader import obtener_estadisticas
from src.recommender import recomendar_con_titulos


def _obtener_dataset():
    # Primero se intenta obtener el DataFrame principal ya cargado por app.py.
    df = st.session_state.get("ratings_df")
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df

    # Si no existe directamente, se intenta obtener desde el diccionario general.
    datos = st.session_state.get("datos")
    if isinstance(datos, dict):
        df = datos.get("df")
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df

    return None


def _graficar_distribucion_ratings(df):
    """Grafica la distribucion general de calificaciones."""
    # Cuenta cuantas veces aparece cada rating de 1 a 5.
    # Esto permite analizar el comportamiento general de valoraciones del dataset.
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
    # Agrupa por titulo y cuenta cuantas valoraciones tiene cada pelicula.
    # No mide si son mejores peliculas, sino cuales fueron mas evaluadas.
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
    # Calcula promedio de rating y cantidad de valoraciones por pelicula.
    resumen = (
        df.groupby("title")
        .agg(
            promedio_rating=("rating", "mean"),
            cantidad_valoraciones=("rating", "count"),
        )
        .reset_index()
    )

    # Se filtran peliculas con pocas valoraciones para evitar promedios poco confiables.
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

    # Estadisticas generales calculadas en data_loader.py.
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

    st.subheader("Matriz usuario-pelicula real")
    _mostrar_matriz_usuario_pelicula_real(df)

    st.divider()

    st.subheader("Distribucion de ratings")
    _graficar_distribucion_ratings(df)

    st.divider()

    st.subheader("Peliculas con mas valoraciones")
    _graficar_peliculas_mas_valoradas(df)

    st.divider()

    st.subheader("Peliculas mejor evaluadas")
    st.write(
        "Se consideran solo peliculas con al menos 50 valoraciones para evitar "
        "promedios poco representativos."
    )
    _mostrar_mejores_promedios(df)

    st.divider()

    st.subheader("Frecuencia de peliculas recomendadas")
    _graficar_frecuencia_recomendaciones(df)

    # Tabla larga del dataset procesado: cada fila es una valoracion real.
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


def _mostrar_matriz_usuario_pelicula_real(df):
    """Muestra una muestra densa de la matriz usuario-pelicula real."""
    datos = st.session_state.get("datos")

    if not isinstance(datos, dict):
        st.warning("No se encontró la matriz usuario-pelicula cargada.")
        return

    # Esta matriz se construye en data_loader.py con pivot_table.
    # Filas: usuarios. Columnas: peliculas. Celdas: ratings.
    matriz = datos.get("matriz")

    if not isinstance(matriz, pd.DataFrame) or matriz.empty:
        st.warning("La matriz usuario-pelicula está vacía.")
        return

    st.write(
        "Esta matriz se construye a partir del dataset procesado. "
        "Cada fila representa un usuario, cada columna representa una película "
        "y cada celda contiene el rating asignado por ese usuario."
    )

    col1, col2 = st.columns(2)

    with col1:
        filas = st.slider(
            "Usuarios a mostrar",
            min_value=3,
            max_value=20,
            value=10,
            step=1,
            key="filas_matriz_real_analisis",
        )

    with col2:
        columnas = st.slider(
            "Películas a mostrar",
            min_value=3,
            max_value=20,
            value=10,
            step=1,
            key="columnas_matriz_real_analisis",
        )

    # Selecciona usuarios con mas ratings para que la matriz mostrada no quede tan vacia.
    usuarios_mas_activos = (
        matriz.notna()
        .sum(axis=1)
        .sort_values(ascending=False)
        .head(filas)
        .index
    )

    # Selecciona peliculas con mas ratings para obtener una muestra mas densa.
    peliculas_mas_valoradas = (
        matriz.notna()
        .sum(axis=0)
        .sort_values(ascending=False)
        .head(columnas)
        .index
    )

    muestra = matriz.loc[usuarios_mas_activos, peliculas_mas_valoradas].copy()

    # Traduce movieId a titulo para que la matriz sea legible.
    mapa_titulos = (
        df[["movieId", "title"]]
        .drop_duplicates()
        .set_index("movieId")["title"]
        .to_dict()
    )

    muestra.columns = [
        mapa_titulos.get(movie_id, movie_id)
        for movie_id in muestra.columns
    ]

    # Densidad: porcentaje de celdas con rating dentro de la muestra seleccionada.
    total_celdas = muestra.shape[0] * muestra.shape[1]
    celdas_con_rating = int(muestra.notna().sum().sum())
    densidad_muestra = round((celdas_con_rating / total_celdas) * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Usuarios mostrados", muestra.shape[0])
    col2.metric("Películas mostradas", muestra.shape[1])
    col3.metric("Densidad de la muestra", f"{densidad_muestra}%")

    # Solo para visualizacion: cambia NaN por "—".
    # La matriz original sigue siendo numerica para los calculos matematicos.
    muestra_visual = muestra.copy()
    muestra_visual = muestra_visual.apply(
        lambda columna: columna.map(
            lambda valor: "—" if pd.isna(valor) else str(int(valor))
        )
    )

    st.dataframe(
        muestra_visual,
        use_container_width=True,
    )

    st.caption(
        "Para que la visualización sea más clara, la app muestra usuarios con muchas "
        "valoraciones y películas con muchas valoraciones. Así se puede observar mejor "
        "cómo funciona la matriz usuario-película real."
    )


def _graficar_frecuencia_recomendaciones(df):
    """Genera recomendaciones para una muestra de usuarios y grafica las mas frecuentes."""
    datos = st.session_state.get("datos")

    if not isinstance(datos, dict):
        st.warning("No hay datos suficientes para generar la frecuencia de recomendaciones.")
        return

    matriz = datos["matriz"]
    similitud = datos["similitud"]

    st.write(
        "Este gráfico genera recomendaciones para una muestra de usuarios y cuenta "
        "qué películas aparecen con mayor frecuencia como recomendadas."
    )

    n_usuarios = st.slider(
        "Usuarios usados para esta prueba",
        min_value=5,
        max_value=50,
        value=10,
        step=5,
        key="usuarios_prueba_frecuencia",
    )

    usuarios = list(matriz.index[:n_usuarios])
    recomendaciones_generales = []

    # Para cada usuario de la muestra, se usa el recomendador real del sistema.
    # La funcion recomendar_con_titulos() esta definida en src/recommender.py.
    for user_id in usuarios:
        recomendaciones = recomendar_con_titulos(
            user_id=user_id,
            matriz=matriz,
            similitud=similitud,
            df=df,
            k_vecinos=5,
            n_recomendaciones=5,
        )

        if not recomendaciones.empty:
            recomendaciones_generales.append(recomendaciones)

    if not recomendaciones_generales:
        st.info("No se generaron recomendaciones suficientes para esta muestra.")
        return

    recomendaciones_df = pd.concat(recomendaciones_generales, ignore_index=True)

    # Cuenta cuantas veces aparece cada pelicula como recomendacion.
    frecuencia = (
        recomendaciones_df["title"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    frecuencia.plot(kind="barh", ax=ax)

    ax.set_title("Peliculas recomendadas con mayor frecuencia")
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel("Pelicula")
    ax.grid(axis="x", alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "La frecuencia indica cuántas veces una película fue recomendada dentro "
        "de la muestra de usuarios analizada."
    )