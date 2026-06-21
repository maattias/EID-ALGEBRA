import numpy as np
import pandas as pd

# =====================================================================
# FUNCIONES AUXILIARES PARA TAB MATEMÁTICO
# =====================================================================

def calculate_dot_product(u, v):
#   Calcula el producto punto entre dos vectores (rellenando NaNs con 0)
    u_clean = np.nan_to_num(u, nan=0.0)
    v_clean = np.nan_to_num(v, nan=0.0)
    return np.dot(u_clean, v_clean)

def calculate_norm(v):
#   Calcula la norma (longitud) de un vector Euclidiano
    v_clean = np.nan_to_num(v, nan=0.0)
    return np.linalg.norm(v_clean)

def get_cosine_similarity_steps(u, v):
    """
    Retorna el desglose del cálculo de similitud coseno entre dos usuarios.
    Esta función expone los valores intermedios para la interfaz de Streamlit.
    """
    dot_prod = calculate_dot_product(u, v)
    norm_u = calculate_norm(u)
    norm_v = calculate_norm(v)
    
    # Prevenir división por cero si un usuario no tiene calificaciones
    if norm_u == 0 or norm_v == 0:
        sim = 0.0
    else:
        sim = dot_prod / (norm_u * norm_v)
        
    return {
        "dot_product": dot_prod,
        "norm_u": norm_u,
        "norm_v": norm_v,
        "similarity": sim
    }

# =====================================================================
# calculate_similarity_matrix(matrix)
# =====================================================================

def calculate_similarity_matrix(matrix):
    """
    Calcula la matriz de similitud coseno completa entre todos los usuarios.

    Args:
        matrix (pd.DataFrame): Matriz usuario-producto (pivot table con NaNs).
        
    Returns:
        pd.DataFrame: Matriz simétrica NxN de similitudes.
    """
    # Rellenamos los NaN (películas no vistas) con 0
    mat_filled = matrix.fillna(0)
    
    mat_np = mat_filled.values # arreglo de NumPy para eficiencia
    
    # 2. Numerador: Producto punto de todos los vectores (u dot v)
    # Al multiplicar la matriz por su transpuesta, obtenemos los N x N productos punto
    dot_product = np.dot(mat_np, mat_np.T)
    
    # 3. Denominador: Cálculo de las normas (||u|| * ||v||)
    norms = np.linalg.norm(mat_np, axis=1)
    norm_matrix = np.outer(norms, norms)
    
    # Prevención de división por cero (reemplazamos ceros por 1e-9)
    norm_matrix = np.where(norm_matrix == 0, 1e-9, norm_matrix)
    
    sim_matrix_np = dot_product / norm_matrix # Matriz de Similitud Coseno
    
    sim_matrix_df = pd.DataFrame( # DataFrame estructurado y simétrico N x N
        sim_matrix_np, 
        index=matrix.index,   # Las filas son los IDs de usuario
        columns=matrix.index  # Las columnas son los mismos IDs de usuario
    )
    
    return sim_matrix_df