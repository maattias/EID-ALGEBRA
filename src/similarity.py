import numpy as np
import pandas as pd

# Funciones auxiliares para el Tab Matemático (Colaboración con Ariel)
def calculate_dot_product(u, v):
    u_clean = np.nan_to_num(u, nan=0.0)
    v_clean = np.nan_to_num(v, nan=0.0)
    return np.dot(u_clean, v_clean)

def calculate_norm(v):
    v_clean = np.nan_to_num(v, nan=0.0)
    return np.linalg.norm(v_clean)

def get_cosine_similarity_steps(u, v):
    dot_prod = calculate_dot_product(u, v)
    norm_u = calculate_norm(u)
    norm_v = calculate_norm(v)
    sim = 0.0 if (norm_u == 0 or norm_v == 0) else dot_prod / (norm_u * norm_v)
    return {"dot_product": dot_prod, "norm_u": norm_u, "norm_v": norm_v, "similarity": sim}

# Función principal que usa Matías
def calcular_matriz_similitud(matriz):
    """Calcula la matriz simétrica de similitud coseno entre usuarios."""
    mat_filled = matriz.fillna(0)
    mat_np = mat_filled.values
    
    dot_product = np.dot(mat_np, mat_np.T)
    norms = np.linalg.norm(mat_np, axis=1)
    norm_matrix = np.outer(norms, norms)
    norm_matrix = np.where(norm_matrix == 0, 1e-9, norm_matrix)
    
    sim_matrix_np = dot_product / norm_matrix
    
    return pd.DataFrame(
        sim_matrix_np, 
        index=matriz.index,
        columns=matriz.index
    )