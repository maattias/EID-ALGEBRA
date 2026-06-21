import numpy as np
import pandas as pd

def obtener_k_vecinos(user_id, similitud, k_vecinos):
#   Dado un usuario objetivo, encuentra los K usuarios más similares
    user_sims = similitud.loc[user_id].drop(user_id)
    return user_sims.sort_values(ascending=False).head(k_vecinos)

def predecir_scores(user_id, neighbors, matriz):
    """
    Calcula el puntaje predicho para todas las películas, ponderando 
    los ratings de los vecinos por su nivel de similitud.
    """
    neighbors_ratings = matriz.loc[neighbors.index]
    weighted_ratings = neighbors_ratings.multiply(neighbors, axis='index')
    sum_weighted_ratings = weighted_ratings.sum(axis=0, skipna=True)
    
    has_rated_mask = neighbors_ratings.notna()
    sum_of_similarities = has_rated_mask.multiply(neighbors, axis='index').sum(axis=0)
    sum_of_similarities = sum_of_similarities.replace(0, np.nan)
    
    return sum_weighted_ratings / sum_of_similarities

def recomendar(user_id, matriz, similitud, k_vecinos=5, n_recomendaciones=10):
    """
    Función orquestadora que identifica películas no vistas por el usuario
    y retorna el Top N ordenado por score predicho.
    """
    neighbors = obtener_k_vecinos(user_id, similitud, k_vecinos)
    predicted_scores = predecir_scores(user_id, neighbors, matriz)
    
    user_ratings = matriz.loc[user_id]
    unseen_movies_mask = user_ratings.isna()
    
    recommendations = predicted_scores[unseen_movies_mask].dropna()
    return recommendations.sort_values(ascending=False).head(n_recomendaciones)