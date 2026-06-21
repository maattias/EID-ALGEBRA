import pandas as pd

def cargar_datos(filepath):
    """Lee el dataset, limpia nulos y filtra usuarios con < 20 valoraciones."""
    column_names = ['userId', 'movieId', 'rating', 'timestamp']
    df = pd.read_csv(filepath, sep='\t', names=column_names)
    df = df.dropna()
    user_counts = df['userId'].value_counts()
    valid_users = user_counts[user_counts >= 20].index
    return df[df['userId'].isin(valid_users)]

def construir_matriz(df):
    """Construye la matriz usuario-producto (pivot table)."""
    return df.pivot(index='userId', columns='movieId', values='rating')

# =====================================================================
# FUNCIONES AUXILIARES PARA SIDEBAR 
# =====================================================================
def obtener_lista_usuarios(df):
    """Retorna una lista ordenada de todos los IDs de usuario."""
    return sorted(df['userId'].unique().tolist())

def obtener_estadisticas(df):
    """Retorna un diccionario con las métricas del dataset."""
    return {
        "total_usuarios": df['userId'].nunique(),
        "total_peliculas": df['movieId'].nunique(),
        "total_valoraciones": len(df)
    }

def obtener_peliculas_usuario(df, user_id):
    """Retorna el historial de películas valoradas por un usuario en específico."""
    return df[df['userId'] == user_id]