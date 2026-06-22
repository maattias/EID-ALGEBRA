#src/data_loader.py

from pathlib import Path
import pandas as pd

DATASET_PATH = Path("data/ml-100k")


def get_dataset_path() -> Path:
    """Valida y retorna la ruta del dataset MovieLens 100K."""
    required_files = ["u.data", "u.item", "u.user"]

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"No existe la carpeta {DATASET_PATH}.")

    missing_files = [
        filename for filename in required_files
        if not (DATASET_PATH / filename).exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Faltan archivos del dataset: " + ", ".join(missing_files)
        )
    return DATASET_PATH


def load_and_clean_data(filepath=None, min_ratings_per_user=20):
    """Carga las valoraciones desde u.data y filtra usuarios con pocas valoraciones."""
    if filepath is None:
        filepath = get_dataset_path() / "u.data"

    df = pd.read_csv(
        filepath,
        sep="\t",
        names=["userId", "movieId", "rating", "timestamp"],
        encoding="latin-1",
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
    """Carga los identificadores y titulos de peliculas desde u.item."""
    if filepath is None:
        filepath = get_dataset_path() / "u.item"

    movies = pd.read_csv(
        filepath,
        sep="|",
        header=None,
        encoding="latin-1",
        usecols=[0, 1],
    )

    movies.columns = ["movieId", "title"]

    movies = movies.dropna()
    movies["movieId"] = movies["movieId"].astype(int)
    movies["title"] = movies["title"].astype(str)

    return movies.reset_index(drop=True)


def load_users(filepath=None):
    """Carga la informacion demografica de usuarios desde u.user."""
    if filepath is None:
        filepath = get_dataset_path() / "u.user"

    users = pd.read_csv(
        filepath,
        sep="|",
        header=None,
        encoding="latin-1",
        names=["userId", "age", "gender", "occupation", "zipCode"],
    )

    users = users.dropna()
    users["userId"] = users["userId"].astype(int)
    users["age"] = users["age"].astype(int)
    users["gender"] = users["gender"].astype(str)
    users["occupation"] = users["occupation"].astype(str)
    users["zipCode"] = users["zipCode"].astype(str)

    return users.reset_index(drop=True)


def load_dataset(ratings_path=None, movies_path=None, users_path=None, min_ratings_per_user=20):
    """Carga ratings, peliculas y usuarios en un unico DataFrame."""
    dataset_path = get_dataset_path()

    if ratings_path is None:
        ratings_path = dataset_path / "u.data"

    if movies_path is None:
        movies_path = dataset_path / "u.item"

    if users_path is None:
        users_path = dataset_path / "u.user"

    ratings = load_and_clean_data(
        filepath=ratings_path,
        min_ratings_per_user=min_ratings_per_user,
    )

    movies = load_movies(movies_path)
    users = load_users(users_path)

    dataset = ratings.merge(movies, on="movieId", how="left")
    dataset = dataset.merge(users, on="userId", how="left")

    dataset = dataset.dropna(
        subset=["userId", "movieId", "rating", "title"]
    )

    return dataset.reset_index(drop=True)


def build_user_item_matrix(df, item_col="movieId"):
    """Construye la matriz usuario-pelicula a partir de las valoraciones."""
    required_columns = {"userId", item_col, "rating"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"El DataFrame debe contener las columnas: {required_columns}"
        )

    matrix = df.pivot_table(
        index="userId",
        columns=item_col,
        values="rating",
        aggfunc="mean",
    )

    matrix = matrix.sort_index(axis=0)
    matrix = matrix.sort_index(axis=1)

    return matrix


def get_dataset_summary(df):
    """Retorna estadisticas generales del dataset."""
    return {
        "users": int(df["userId"].nunique()),
        "movies": int(df["movieId"].nunique()),
        "ratings": int(len(df)),
        "avg_rating": float(df["rating"].mean()),
        "min_rating": float(df["rating"].min()),
        "max_rating": float(df["rating"].max()),
    }


def get_movie_title_map(movies_df=None):
    """Retorna un diccionario para traducir movieId a title."""
    if movies_df is None:
        movies_df = load_movies()

    return dict(zip(movies_df["movieId"], movies_df["title"]))


def obtener_lista_usuarios(df):
    """Retorna la lista ordenada de usuarios disponibles."""
    return sorted(df["userId"].unique().tolist())


def obtener_peliculas_usuario(df, user_id):
    """Retorna las peliculas valoradas por un usuario especifico."""
    return df[df["userId"] == user_id].copy()


def obtener_estadisticas(df):
    """Retorna estadisticas resumidas para la interfaz."""
    n_usuarios = df["userId"].nunique()
    n_peliculas = df["movieId"].nunique()
    n_valoraciones = len(df)

    total_posibles = n_usuarios * n_peliculas

    if total_posibles == 0:
        densidad = 0.0
    else:
        densidad = round((n_valoraciones / total_posibles) * 100, 2)

    return {
        "n_usuarios": int(n_usuarios),
        "n_peliculas": int(n_peliculas),
        "n_valoraciones": int(n_valoraciones),
        "densidad": densidad,
    }