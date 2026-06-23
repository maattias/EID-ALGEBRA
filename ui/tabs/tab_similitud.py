# ui/tabs/tab_similitud.py

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.model.similarity import calcular_matriz_similitud
from src.recommender import obtener_k_vecinos


def _obtener_datos():
    """Obtiene los datos cargados desde session_state."""
    datos = st.session_state.get("datos")

    if not isinstance(datos, dict):
        return None

    return datos


def _obtener_matriz_similitud(datos):
    """Retorna la matriz de similitud ya calculada o la recalcula si no existe."""
    matriz = datos["matriz"]
    similitud = datos.get("similitud")

    # app.py normalmente ya calcula esta matriz al iniciar la app.
    if isinstance(similitud, pd.DataFrame) and not similitud.empty:
        return similitud

    # Si no existe, se calcula usando la funcion matematica de src/model/similarity.py.
    return calcular_matriz_similitud(matriz)


def _obtener_usuario_seleccionado(similitud):
    """Retorna el usuario seleccionado desde session_state."""
    user_id = st.session_state.get("selected_user")

    if user_id in similitud.index:
        return user_id

    try:
        user_id = int(user_id)

        if user_id in similitud.index:
            return user_id
    except (TypeError, ValueError):
        pass

    # Si el usuario seleccionado no existe, se usa el primer usuario disponible.
    return similitud.index[0]


def _graficar_heatmap(similitud, muestra):
    """Grafica un mapa de calor de similitud entre usuarios."""
    # Se toma una submatriz para no graficar los 943 usuarios completos.
    muestra = min(int(muestra), len(similitud))
    muestra_df = similitud.iloc[:muestra, :muestra]

    fig, ax = plt.subplots(figsize=(8, 6))

    # El heatmap representa la matriz de similitud coseno.
    # Cada celda indica que tan parecidos son dos usuarios.
    imagen = ax.imshow(
        muestra_df.values,
        aspect="auto",
        vmin=0,
        vmax=1,
    )

    ax.set_title("Mapa de calor de similitud coseno")
    ax.set_xlabel("Usuarios")
    ax.set_ylabel("Usuarios")

    ax.set_xticks(range(len(muestra_df.columns)))
    ax.set_xticklabels(muestra_df.columns, rotation=90, fontsize=8)

    ax.set_yticks(range(len(muestra_df.index)))
    ax.set_yticklabels(muestra_df.index, fontsize=8)

    fig.colorbar(imagen, ax=ax, label="Similitud coseno")

    st.pyplot(fig)
    plt.close(fig)


def _mostrar_usuarios_similares(similitud, user_id, k_vecinos):
    """Muestra los usuarios mas similares al usuario objetivo."""
    # obtener_k_vecinos() esta definida en src/recommender.py.
    # Usa la matriz de similitud para buscar los usuarios con mayor coseno.
    vecinos = obtener_k_vecinos(
        user_id=user_id,
        similitud=similitud,
        k_vecinos=k_vecinos,
    )

    if vecinos.empty:
        st.info("No se encontraron usuarios similares.")
        return

    vecinos_df = vecinos.reset_index()
    vecinos_df.columns = ["Usuario", "Similitud coseno"]
    vecinos_df["Similitud coseno"] = vecinos_df["Similitud coseno"].round(4)

    st.dataframe(
        vecinos_df,
        use_container_width=True,
        hide_index=True,
    )


def _graficar_comparacion_perfiles(matriz, similitud, user_id, df):
    """Compara ratings comunes entre el usuario objetivo y su vecino mas cercano."""
    # Se obtiene solo el vecino mas cercano para comparar perfiles de forma visual.
    vecinos = obtener_k_vecinos(
        user_id=user_id,
        similitud=similitud,
        k_vecinos=1,
    )

    if vecinos.empty:
        st.info("No existe un vecino similar para comparar.")
        return

    vecino_id = vecinos.index[0]
    valor_similitud = vecinos.iloc[0]

    # Cada fila de la matriz usuario-pelicula representa un vector de preferencias.
    ratings_usuario = matriz.loc[user_id]
    ratings_vecino = matriz.loc[vecino_id]

    # Se comparan solo peliculas que ambos usuarios valoraron.
    peliculas_comunes = ratings_usuario.notna() & ratings_vecino.notna()

    comparacion = pd.DataFrame(
        {
            f"Usuario {user_id}": ratings_usuario[peliculas_comunes],
            f"Vecino {vecino_id}": ratings_vecino[peliculas_comunes],
        }
    )

    if comparacion.empty:
        st.info(
            f"El usuario {user_id} y el usuario {vecino_id} no tienen peliculas valoradas en comun."
        )
        return

    # Diferencia absoluta entre ratings.
    # Sirve para ver que tan parecidas fueron sus valoraciones en peliculas comunes.
    comparacion["diferencia"] = (
        comparacion[f"Usuario {user_id}"] - comparacion[f"Vecino {vecino_id}"]
    ).abs()

    total_comunes = len(comparacion)
    diferencia_promedio = round(comparacion["diferencia"].mean(), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Similitud coseno", f"{valor_similitud:.4f}")
    col2.metric("Peliculas en comun", total_comunes)
    col3.metric("Diferencia promedio", diferencia_promedio)

    st.caption(
        "El grafico muestra solo las 10 peliculas comunes con menor diferencia de rating. "
        "No representa todas las peliculas valoradas por ambos usuarios."
    )

    # Se toman las 10 peliculas donde ambos usuarios tuvieron ratings mas parecidos.
    comparacion_grafico = comparacion.sort_values("diferencia").head(10)
    comparacion_grafico = comparacion_grafico.drop(columns=["diferencia"])

    # Traduce movieId a titulo de pelicula.
    mapa_titulos = (
        df[["movieId", "title"]]
        .drop_duplicates()
        .set_index("movieId")["title"]
        .to_dict()
    )

    comparacion_grafico.index = [
        mapa_titulos.get(movie_id, movie_id)
        for movie_id in comparacion_grafico.index
    ]

    fig, ax = plt.subplots(figsize=(9, 5))
    comparacion_grafico.plot(kind="bar", ax=ax)

    ax.set_title(
        f"10 peliculas comunes mas parecidas: usuario {user_id} vs vecino {vecino_id}"
    )
    ax.set_xlabel("Peliculas")
    ax.set_ylabel("Rating")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

    # Tabla completa con todas las peliculas comunes usadas en la comparacion.
    with st.expander("Ver todas las peliculas comunes comparadas"):
        tabla = comparacion.copy()

        tabla.index = [
            mapa_titulos.get(movie_id, movie_id)
            for movie_id in tabla.index
        ]

        tabla = tabla.sort_values("diferencia")

        st.dataframe(
            tabla,
            use_container_width=True,
        )


def render_tab_similitud():
    """Muestra el analisis de similitud entre usuarios."""
    datos = _obtener_datos()

    if datos is None:
        st.error("No hay datos cargados en session_state.")
        return

    df = datos["df"]
    matriz = datos["matriz"]

    # Matriz cuadrada donde filas y columnas son usuarios.
    # Cada celda contiene la similitud coseno entre dos usuarios.
    similitud = _obtener_matriz_similitud(datos)

    user_id = _obtener_usuario_seleccionado(similitud)

    # Parametros definidos desde el sidebar.
    muestra = st.session_state.get("sample_size", 20)
    k_vecinos = st.session_state.get("k_vecinos_similitud", 5)

    st.header("Similitud entre usuarios")

    st.write(
        "Esta seccion usa la matriz usuario-pelicula real del dataset para comparar "
        "usuarios mediante similitud coseno."
    )

    st.subheader("Mapa de calor de similitud")
    _graficar_heatmap(similitud, muestra)

    st.subheader(f"Usuarios mas similares al usuario {user_id}")
    _mostrar_usuarios_similares(similitud, user_id, k_vecinos)

    st.subheader("Comparacion con el vecino mas cercano")
    _graficar_comparacion_perfiles(matriz, similitud, user_id, df)