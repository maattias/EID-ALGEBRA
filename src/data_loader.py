#src/data_loader.py

from pathlib import Path
import pandas as pd

RUTA_DATASET = Path("data/ml-100k")

def obtener_ruta_dataset() -> Path:
    """Valida y retorna la ruta del dataset MovieLens 100K."""
    archivos_requeridos = ["u.data", "u.item", "u.user"]

    if not RUTA_DATASET.exists():
        raise FileNotFoundError(f"No existe la carpeta {RUTA_DATASET}.")

    archivos_faltantes = [
        archivo for archivo in archivos_requeridos
        if not (RUTA_DATASET / archivo).exists()
    ]

    if archivos_faltantes:
        raise FileNotFoundError(
            "Faltan archivos del dataset: " + ", ".join(archivos_faltantes)
        )

    return RUTA_DATASET


def cargar_y_limpiar_valoraciones(ruta_archivo=None, minimo_valoraciones_usuario=20):
    """Carga las valoraciones desde u.data y filtra usuarios con pocas valoraciones."""
    if ruta_archivo is None:
        ruta_archivo = obtener_ruta_dataset() / "u.data"

    df = pd.read_csv(
        ruta_archivo,
        sep="\t",
        names=["userId", "movieId", "rating", "timestamp"],
        encoding="latin-1",
    )

    df = df.dropna()

    df["userId"] = df["userId"].astype(int)
    df["movieId"] = df["movieId"].astype(int)
    df["rating"] = df["rating"].astype(float)
    df["timestamp"] = df["timestamp"].astype(int)

    if minimo_valoraciones_usuario > 1:
        conteo_usuarios = df["userId"].value_counts()
        usuarios_validos = conteo_usuarios[
            conteo_usuarios >= minimo_valoraciones_usuario
        ].index

        df = df[df["userId"].isin(usuarios_validos)]

    return df.reset_index(drop=True)


def cargar_peliculas(ruta_archivo=None):
    """Carga los identificadores y titulos de peliculas desde u.item."""
    if ruta_archivo is None:
        ruta_archivo = obtener_ruta_dataset() / "u.item"

    peliculas = pd.read_csv(
        ruta_archivo,
        sep="|",
        header=None,
        encoding="latin-1",
        usecols=[0, 1],
    )

    peliculas.columns = ["movieId", "title"]

    peliculas = peliculas.dropna()
    peliculas["movieId"] = peliculas["movieId"].astype(int)
    peliculas["title"] = peliculas["title"].astype(str)

    return peliculas.reset_index(drop=True)


def cargar_usuarios(ruta_archivo=None):
    """Carga la informacion demografica de usuarios desde u.user."""
    if ruta_archivo is None:
        ruta_archivo = obtener_ruta_dataset() / "u.user"

    usuarios = pd.read_csv(
        ruta_archivo,
        sep="|",
        header=None,
        encoding="latin-1",
        names=["userId", "age", "gender", "occupation", "zipCode"],
    )

    usuarios = usuarios.dropna()

    usuarios["userId"] = usuarios["userId"].astype(int)
    usuarios["age"] = usuarios["age"].astype(int)
    usuarios["gender"] = usuarios["gender"].astype(str)
    usuarios["occupation"] = usuarios["occupation"].astype(str)
    usuarios["zipCode"] = usuarios["zipCode"].astype(str)

    return usuarios.reset_index(drop=True)

def cargar_dataset(
    ruta_valoraciones=None,
    ruta_peliculas=None,
    ruta_usuarios=None,
    minimo_valoraciones_usuario=20,
):
    """Carga valoraciones, peliculas y usuarios en un unico DataFrame."""
    ruta_dataset = obtener_ruta_dataset()

    if ruta_valoraciones is None:
        ruta_valoraciones = ruta_dataset / "u.data"

    if ruta_peliculas is None:
        ruta_peliculas = ruta_dataset / "u.item"

    if ruta_usuarios is None:
        ruta_usuarios = ruta_dataset / "u.user"

    valoraciones = cargar_y_limpiar_valoraciones(
        ruta_archivo=ruta_valoraciones,
        minimo_valoraciones_usuario=minimo_valoraciones_usuario,
    )

    peliculas = cargar_peliculas(ruta_peliculas)
    usuarios = cargar_usuarios(ruta_usuarios)

    dataset = valoraciones.merge(peliculas, on="movieId", how="left")
    dataset = dataset.merge(usuarios, on="userId", how="left")

    dataset = dataset.dropna(
        subset=["userId", "movieId", "rating", "title"]
    )

    return dataset.reset_index(drop=True)


def construir_matriz_usuario_pelicula(df, columna_item="movieId"):
    """Construye la matriz usuario-pelicula a partir de las valoraciones."""
    columnas_requeridas = {"userId", columna_item, "rating"}

    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(
            f"El DataFrame debe contener las columnas: {columnas_requeridas}"
        )

    matriz = df.pivot_table(
        index="userId",
        columns=columna_item,
        values="rating",
        aggfunc="mean",
    )

    matriz = matriz.sort_index(axis=0)
    matriz = matriz.sort_index(axis=1)

    return matriz


def obtener_resumen_dataset(df):
    """Retorna estadisticas generales del dataset."""
    return {
        "usuarios": int(df["userId"].nunique()),
        "peliculas": int(df["movieId"].nunique()),
        "valoraciones": int(len(df)),
        "promedio_rating": float(df["rating"].mean()),
        "rating_minimo": float(df["rating"].min()),
        "rating_maximo": float(df["rating"].max()),
    }


def obtener_mapa_titulos(peliculas_df=None):
    """Retorna un diccionario para traducir movieId a title."""
    if peliculas_df is None:
        peliculas_df = cargar_peliculas()

    return dict(zip(peliculas_df["movieId"], peliculas_df["title"]))


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