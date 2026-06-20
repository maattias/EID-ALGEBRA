import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    """
    Args:
        filepath (str): Ruta al archivo u.data
        
    Returns:
        pd.DataFrame: DataFrame limpio con columnas ['userId', 'movieId', 'rating', 'timestamp']
    """
    # Leer el archivo. Según el README de MovieLens, está separado por tabulaciones ('\t')
    column_names = ['userId', 'movieId', 'rating', 'timestamp']
    df = pd.read_csv(filepath, sep='\t', names=column_names)
    
    # Limpiar datos nulos (por si acaso el dataset tuviera errores de lectura)
    df = df.dropna()
    
    # Filtrar usuarios con menos de 20 valoraciones 
    user_counts = df['userId'].value_counts()
    valid_users = user_counts[user_counts >= 20].index
    df_filtered = df[df['userId'].isin(valid_users)]
    
    return df_filtered

def build_user_item_matrix(df):
    """
    Args:
        df (pd.DataFrame): DataFrame limpio retornado por load_and_clean_data.
        
    Returns:
        pd.DataFrame: Matriz con usuarios en filas, películas en columnas y 
                      ratings como valores (NaN donde no hay valoración).
    """
    # Crear la tabla pivote
                                # Filas         # Columnas         # Valores
    user_item_matrix = df.pivot(index='userId', columns='movieId', values='rating')
    
    return user_item_matrix

# ==========================================
# if __name__ == "__main__":
#     ruta_archivo = "../data/raw/u.data"
#     df_limpio = load_and_clean_data(ruta_archivo)
#     matriz = build_user_item_matrix(df_limpio)
#     print("Forma de la matriz:", matriz.shape)
#     print(matriz.head())
# ==========================================