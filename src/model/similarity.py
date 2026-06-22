#src/model/similarity.py

import numpy as np
import pandas as pd


def calculate_dot_product(u, v):
    """Calcula el producto punto entre dos vectores."""
    u_clean = np.nan_to_num(u, nan=0.0)
    v_clean = np.nan_to_num(v, nan=0.0)

    return float(np.dot(u_clean, v_clean))


def calculate_norm(v):
    """Calcula la norma euclidiana de un vector."""
    v_clean = np.nan_to_num(v, nan=0.0)

    return float(np.linalg.norm(v_clean))


def calculate_cosine_similarity(u, v):
    """Calcula la similitud coseno entre dos vectores."""
    dot_product = calculate_dot_product(u, v)
    norm_u = calculate_norm(u)
    norm_v = calculate_norm(v)

    if norm_u == 0 or norm_v == 0:
        return 0.0

    similarity = dot_product / (norm_u * norm_v)

    return float(np.clip(similarity, -1.0, 1.0))


def get_cosine_similarity_steps(u, v):
    """Retorna los valores intermedios del calculo de similitud coseno."""
    dot_product = calculate_dot_product(u, v)
    norm_u = calculate_norm(u)
    norm_v = calculate_norm(v)

    if norm_u == 0 or norm_v == 0:
        similarity = 0.0
    else:
        similarity = dot_product / (norm_u * norm_v)

    return {
        "dot_product": float(dot_product),
        "norm_u": float(norm_u),
        "norm_v": float(norm_v),
        "similarity": float(np.clip(similarity, -1.0, 1.0)),
    }


def calculate_similarity_matrix(matrix):
    """Calcula la matriz de similitud coseno entre usuarios."""
    if not isinstance(matrix, pd.DataFrame):
        raise TypeError("La matriz debe ser un DataFrame de pandas.")

    if matrix.empty:
        raise ValueError("La matriz usuario-pelicula esta vacia.")

    matrix_filled = matrix.fillna(0)
    matrix_np = matrix_filled.to_numpy(dtype=float)

    dot_products = np.dot(matrix_np, matrix_np.T)
    norms = np.linalg.norm(matrix_np, axis=1)
    norm_products = np.outer(norms, norms)

    similarity_np = np.divide(
        dot_products,
        norm_products,
        out=np.zeros_like(dot_products, dtype=float),
        where=norm_products != 0,
    )

    similarity_np = np.clip(similarity_np, -1.0, 1.0)

    return pd.DataFrame(
        similarity_np,
        index=matrix.index,
        columns=matrix.index,
    )