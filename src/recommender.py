#src/recommender.py

import numpy as np
import pandas as pd


def obtener_k_vecinos(user_id, similitud, k_vecinos=5):
    """Obtiene los k usuarios mas similares al usuario objetivo."""
    
    if user_id not in similitud.index:
        raise ValueError(f"El usuario {user_id} no existe en la matriz de similitud.")

    user_sims = similitud.loc[user_id].drop(index=user_id)
    user_sims = user_sims[user_sims > 0]

    return user_sims.sort_values(ascending=False).head(k_vecinos)


def predecir_scores(user_id, neighbors, matriz):
    """Predice puntajes usando promedio ponderado por similitud coseno."""
    if user_id not in matriz.index:
        raise ValueError(f"El usuario {user_id} no existe en la matriz usuario-pelicula.")

    if neighbors.empty:
        return pd.Series(dtype=float, name="score_predicho")

    neighbors_ratings = matriz.loc[neighbors.index]

    weighted_ratings = neighbors_ratings.multiply(neighbors, axis="index")
    sum_weighted_ratings = weighted_ratings.sum(axis=0, skipna=True)

    rated_mask = neighbors_ratings.notna()
    sum_similarities = rated_mask.multiply(neighbors, axis="index").sum(axis=0)
    sum_similarities = sum_similarities.replace(0, np.nan)

    predicted_scores = sum_weighted_ratings / sum_similarities
    predicted_scores.name = "score_predicho"

    return predicted_scores


def recomendar(user_id, matriz, similitud, k_vecinos=5, n_recomendaciones=10):
    """Genera recomendaciones para peliculas que el usuario aun no ha valorado."""
    neighbors = obtener_k_vecinos(
        user_id=user_id,
        similitud=similitud,
        k_vecinos=k_vecinos,
    )

    predicted_scores = predecir_scores(
        user_id=user_id,
        neighbors=neighbors,
        matriz=matriz,
    )

    if predicted_scores.empty:
        return pd.Series(dtype=float, name="score_predicho")

    user_ratings = matriz.loc[user_id]
    unseen_mask = user_ratings.isna()

    recommendations = predicted_scores[unseen_mask]
    recommendations = recommendations.dropna()
    recommendations = recommendations.sort_values(ascending=False)

    return recommendations.head(n_recomendaciones)


def recomendar_con_titulos(
    user_id,
    matriz,
    similitud,
    df,
    k_vecinos=5,
    n_recomendaciones=10,
):
    """Genera recomendaciones y agrega el titulo de cada pelicula."""
    recommendations = recomendar(
        user_id=user_id,
        matriz=matriz,
        similitud=similitud,
        k_vecinos=k_vecinos,
        n_recomendaciones=n_recomendaciones,
    )

    if recommendations.empty:
        return pd.DataFrame(columns=["movieId", "title", "score_predicho"])

    title_map = (
        df[["movieId", "title"]]
        .drop_duplicates()
        .set_index("movieId")["title"]
        .to_dict()
    )

    result = recommendations.reset_index()
    result.columns = ["movieId", "score_predicho"]
    result["title"] = result["movieId"].map(title_map)

    result = result[["movieId", "title", "score_predicho"]]
    result["score_predicho"] = result["score_predicho"].round(3)

    return result