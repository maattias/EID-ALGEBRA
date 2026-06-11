import numpy as np

def cosine_similarity(matrix):
    """
    Calcula la matriz de similitud coseno entre usuarios.
    
    Args:
        matrix (np.ndarray o pd.DataFrame): Matriz de interacciones usuario-producto.
        
    Returns:
        np.ndarray: Matriz de similitud de tamaño N x N.
    """
    # 1. Asegurarnos de que los datos estén en formato de arreglo de NumPy
    mat = np.array(matrix)
    
    # 2. Numerador: Producto punto de todos los vectores (u dot v)
    # Multiplicamos la matriz por su transpuesta para obtener las similitudes cruzadas
    dot_product = np.dot(mat, mat.T)
    
    # 3. Denominador: Cálculo de las normas (||u|| y ||v||)
    # Calculamos la norma euclidiana (longitud) de la fila de cada usuario
    norms = np.linalg.norm(mat, axis=1)
    
    # Creamos una matriz con la multiplicación de las normas de cada par de usuarios
    norm_matrix = np.outer(norms, norms)
    
    # Prevención de errores: Evitar división por cero
    # Si un usuario tiene norma 0 (no ha valorado nada), reemplazamos el 0 por un número diminuto
    norm_matrix = np.where(norm_matrix == 0, 1e-9, norm_matrix)
    
    # 4. Cálculo final de la similitud coseno
    sim_matrix = dot_product / norm_matrix
    
    return sim_matrix