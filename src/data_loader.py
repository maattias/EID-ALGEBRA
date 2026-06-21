# src/data_loader.py

from pathlib import Path

import pandas as pd


DATASET_CANDIDATES = [
    Path("data/ml-100k"),
    Path("data/m1-100k"),
]


def get_dataset_path() -> Path:
    """
    Busca automáticamente la carpeta del dataset MovieLens 100K.
    """

    for path in DATASET_CANDIDATES:
        if (path / "u.data").exists() and (path / "u.item").exists():
            return path

    raise FileNotFoundError(
        "No se encontró MovieLens 100K. Debe existir la carpeta "
        "data/ml-100k con los archivos u.data y u.item."
    )


def load_and_clean_data(filepath=None, min_ratings_per_user=20):
    """
    Carga y limpia el archivo u.data.

    """

    if filepath is None:
        filepath = get_dataset_path() / "u.data"

    filepath = Path(filepath)

    column_names = ["userId", "movieId", "rating", "timestamp"]

    df = pd.read_csv(
        filepath,
        sep="\t",
        names=column_names,
        encoding="latin-1"
    )

    df = df.dropna()

    df["userId"] = df["userId"].astype(int)
    df["movieId"] = df["movieId"].astype(int)
    df["rating"] = df["rating"].astype(float)
    df["timestamp"] = df["timestamp"].astype(int)

    if min_ratings_per_user > 1:
        user_counts = df["userId"].value_counts()
        valid_users = user_counts[user_counts >= min_ratings_per_user].index
        df = df[df["userId"].isin(valid_users)]

    return df.reset_index(drop=True)


def load_movies(filepath=None):
    """
    Carga el archivo u.item.
    """

    if filepath is None:
        filepath = get_dataset_path() / "u.item"

    filepath = Path(filepath)

    movies = pd.read_csv(
        filepath,
        sep="|",
        header=None,
        encoding="latin-1",
        usecols=[0, 1],
        names=["movieId", "title"]
    )

    movies = movies.dropna()

    movies["movieId"] = movies["movieId"].astype(int)
    movies["title"] = movies["title"].astype(str)

    return movies.reset_index(drop=True)


def load_users(filepath=None):
    """
    Carga el archivo u.user.
    """

    if filepath is None:
        filepath = get_dataset_path() / "u.user"

    filepath = Path(filepath)

    users = pd.read_csv(
        filepath,
        sep="|",
        header=None,
        encoding="latin-1",
        names=["userId", "age", "gender", "occupation", "zipCode"]
    )

    users = users.dropna()

    users["userId"] = users["userId"].astype(int)
    users["age"] = users["age"].astype(int)

    return users.reset_index(drop=True)


def load_dataset(
    ratings_path=None,
    movies_path=None,
    min_ratings_per_user=20
):
    """
    Carga ratings + títulos de películas.
    """

    dataset_path = get_dataset_path()

    if ratings_path is None:
        ratings_path = dataset_path / "u.data"

    if movies_path is None:
        movies_path = dataset_path / "u.item"

    ratings = load_and_clean_data(
        filepath=ratings_path,
        min_ratings_per_user=min_ratings_per_user
    )

    movies = load_movies(movies_path)

    dataset = ratings.merge(movies, on="movieId", how="left")
    dataset = dataset.dropna(subset=["userId", "movieId", "rating", "title"])

    return dataset.reset_index(drop=True)


def build_user_item_matrix(df, item_col="movieId"):
    """
    Construye la matriz usuario-producto.
    """

    required_columns = {"userId", item_col, "rating"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"El DataFrame debe contener las columnas: {required_columns}"
        )

    user_item_matrix = df.pivot_table(
        index="userId",
        columns=item_col,
        values="rating",
        aggfunc="mean"
    )

    return user_item_matrix


def get_dataset_summary(df):
    """
    Retorna métricas generales del dataset.
    """

    summary = {
        "users": int(df["userId"].nunique()),
        "movies": int(df["movieId"].nunique()),
        "ratings": int(len(df)),
        "avg_rating": float(df["rating"].mean()),
        "min_rating": float(df["rating"].min()),
        "max_rating": float(df["rating"].max()),
    }

    return summary


def get_movie_title_map(movies_df=None):
    """
    Retorna un diccionario para traducir movieId a title.
    """

    if movies_df is None:
        movies_df = load_movies()

    return dict(zip(movies_df["movieId"], movies_df["title"]))

def obtener_lista_usuarios(df):
    """
    Retorna la lista ordenada de usuarios disponibles.
    """
    return sorted(df["userId"].unique().tolist())


def obtener_peliculas_usuario(df, user_id):
    """
    Retorna las películas valoradas por un usuario.
    """
    return df[df["userId"] == user_id].copy()


def obtener_estadisticas(df):
    """
    Retorna estadísticas básicas del dataset para el sidebar.
    """
    n_usuarios = df["userId"].nunique()
    n_peliculas = df["movieId"].nunique()
    n_valoraciones = len(df)

    total_posibles = n_usuarios * n_peliculas

    if total_posibles == 0:
        densidad = 0
    else:
        densidad = round((n_valoraciones / total_posibles) * 100, 2)

    return {
        "n_usuarios": int(n_usuarios),
        "n_peliculas": int(n_peliculas),
        "n_valoraciones": int(n_valoraciones),
        "densidad": densidad,
    }


if __name__ == "__main__":
    df = load_dataset()
    matrix = build_user_item_matrix(df)

    print("Dataset:")
    print(df.head())

    print("\nResumen:")
    print(get_dataset_summary(df))

    print("\nForma de la matriz usuario-producto:")
    print(matrix.shape)