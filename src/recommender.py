"""
Módulo de enrutamiento y predicción de recomendaciones

Utiliza las matrices de datos y de similitud para identificar vecindarios de usuarios,
predecir puntajes mediante combinaciones lineales ponderadas, y generar rankings
"""

import numpy as np
import pandas as pd

def obtener_k_vecinos(user_id, similitud, k_vecinos=5):
    """Obtiene los k usuarios mas similares al usuario objetivo"""
    if user_id not in similitud.index:
        raise ValueError(f"El usuario {user_id} no existe en la matriz de similitud.")

    # Extrae el vector de afinidad y usa .drop() para eliminar la auto-similitud 
    # (coseno de 1.0) evitando que el usuario sea recomendado como vecino de sí mismo
    similitudes_usuario = similitud.loc[user_id].drop(index=user_id)
    similitudes_usuario = similitudes_usuario[similitudes_usuario > 0]

    return similitudes_usuario.sort_values(ascending=False).head(k_vecinos)


def predecir_puntajes(user_id, vecinos, matriz):
    """
    Predice puntajes usando promedio ponderado por similitud coseno.
    La calificación de cada vecino escala proporcionalmente según su grado de 
    similitud con el usuario objetivo. Se ignora a los vecinos que no vieron 
    una película determinada en la normalización
    """
    if user_id not in matriz.index:
        raise ValueError(f"El usuario {user_id} no existe en la matriz usuario-pelicula.")

    if vecinos.empty:
        return pd.Series(dtype=float, name="puntaje_predicho")

    valoraciones_vecinos = matriz.loc[vecinos.index]

    # Proyecta las calificaciones multiplicando por el escalar de similitud (peso del vecino)
    valoraciones_ponderadas = valoraciones_vecinos.multiply(vecinos, axis="index")
    suma_ponderada = valoraciones_ponderadas.sum(axis=0, skipna=True)

    # Crea máscara booleana (.notna()) para aislar exclusivamente a los vecinos que evaluaron 
    # el ítem, impidiendo que los NaN diluyan el denominador de la ponderación
    mascara_valoradas = valoraciones_vecinos.notna()
    suma_similitudes = mascara_valoradas.multiply(vecinos, axis="index").sum(axis=0)
    suma_similitudes = suma_similitudes.replace(0, np.nan)

    puntajes_predichos = suma_ponderada / suma_similitudes
    puntajes_predichos.name = "puntaje_predicho"

    return puntajes_predichos


def recomendar(user_id, matriz, similitud, k_vecinos=5, n_recomendaciones=10):
    """Genera recomendaciones para peliculas que el usuario aun no ha valorado"""
    vecinos = obtener_k_vecinos(
        user_id=user_id,
        similitud=similitud,
        k_vecinos=k_vecinos,
    )

    puntajes_predichos = predecir_puntajes(
        user_id=user_id,
        vecinos=vecinos,
        matriz=matriz,
    )

    if puntajes_predichos.empty:
        return pd.Series(dtype=float, name="puntaje_predicho")

    valoraciones_usuario = matriz.loc[user_id]
    peliculas_no_vistas = valoraciones_usuario.isna()

    recomendaciones = puntajes_predichos[peliculas_no_vistas]
    recomendaciones = recomendaciones.dropna()
    recomendaciones = recomendaciones.sort_values(ascending=False)

    return recomendaciones.head(n_recomendaciones)  # N mejores películas (no vistas por el usuario) ordenadas 
                                                    # descendentemente por su puntaje predicho.


def recomendar_con_titulos(
    user_id,
    matriz,
    similitud,
    df,
    k_vecinos=5,
    n_recomendaciones=10,
):
    """Genera recomendaciones y agrega el titulo de cada pelicula."""
    recomendaciones = recomendar(
        user_id=user_id,
        matriz=matriz,
        similitud=similitud,
        k_vecinos=k_vecinos,
        n_recomendaciones=n_recomendaciones,
    )

    if recomendaciones.empty:
        return pd.DataFrame(columns=["movieId", "title", "puntaje_predicho"])

    mapa_titulos = (
        df[["movieId", "title"]]
        .drop_duplicates()
        .set_index("movieId")["title"]
        .to_dict()
    )

    resultado = recomendaciones.reset_index()
    resultado.columns = ["movieId", "puntaje_predicho"]
    resultado["title"] = resultado["movieId"].map(mapa_titulos)

    resultado = resultado[["movieId", "title", "puntaje_predicho"]]
    resultado["puntaje_predicho"] = resultado["puntaje_predicho"].round(3)

    return resultado