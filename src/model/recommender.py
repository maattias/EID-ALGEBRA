import numpy as np
import pandas as pd

def recommend(user_id, matrix, sim_matrix, k=5, n=10):
    """
    Genera recomendaciones para un usuario basado en los K vecinos más similares.
    
    Args:
        user_id (int o str): Identificador del usuario objetivo (índice en la matriz).
        matrix (pd.DataFrame): Matriz usuario-producto original.
        sim_matrix (np.ndarray): Matriz de similitud NxN.
        k (int): Número de vecinos a considerar.
        n (int): Número de películas a recomendar.
        
    Returns:
        pd.Series: Top N películas recomendadas con su puntaje predicho.
    """
    # 1. Obtener el vector de similitud del usuario objetivo
    # Si user_id es un índice de DataFrame, buscamos su posición numérica
    user_idx = matrix.index.get_loc(user_id) if isinstance(matrix, pd.DataFrame) else user_id
    user_similarities = sim_matrix[user_idx]
    
    # 2. Identificar los K vecinos más similares
    # argsort() ordena de menor a mayor, tomamos los últimos K+1 y evitamos al propio usuario
    nearest_neighbors_idx = np.argsort(user_similarities)[-(k+1):-1][::-1]
    neighbor_similarities = user_similarities[nearest_neighbors_idx]
    
    # 3. Extraer las calificaciones de los vecinos
    # Si matrix es DataFrame, usamos iloc; si es numpy array, indexamos directo
    if isinstance(matrix, pd.DataFrame):
        neighbor_ratings = matrix.iloc[nearest_neighbors_idx].values
    else:
        neighbor_ratings = matrix[nearest_neighbors_idx]
        
    # 4. Ponderar las calificaciones por la similitud (u dot v)
    # Multiplicamos la similitud de cada vecino por sus calificaciones
    weighted_ratings = neighbor_similarities[:, np.newaxis] * neighbor_ratings
    
    # Sumamos los puntajes ponderados para cada película
    sum_weighted_ratings = np.sum(weighted_ratings, axis=0)
    
    # 5. Filtrar las películas que el usuario ya vio
    user_ratings = matrix.iloc[user_idx].values if isinstance(matrix, pd.DataFrame) else matrix[user_idx]
    
    # Ponemos un puntaje de -1 a las películas ya vistas para que no se recomienden
    sum_weighted_ratings[user_ratings > 0] = -1
    
    # 6. Obtener el Top N de películas
    top_n_indices = np.argsort(sum_weighted_ratings)[-n:][::-1]
    
    # 7. Formatear la salida
    if isinstance(matrix, pd.DataFrame):
        recommendations = pd.Series(
            sum_weighted_ratings[top_n_indices], 
            index=matrix.columns[top_n_indices]
        )
    else:
        recommendations = top_n_indices # Retorna solo índices si es numpy array
        
    return recommendations