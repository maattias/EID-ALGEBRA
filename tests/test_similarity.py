import numpy as np
import pandas as pd

from src.model.similarity import (
    calcular_matriz_similitud,
    calcular_norma,
    calcular_producto_punto,
    calcular_similitud_coseno,
)


def test_producto_punto():
    """Verifica el cálculo del producto punto entre dos vectores."""
    u = np.array([1, 2, 3])
    v = np.array([4, 5, 6])

    resultado = calcular_producto_punto(u, v)

    assert np.isclose(resultado, 32.0)


def test_norma_vectorial():
    """Verifica el cálculo de la norma euclidiana."""
    v = np.array([3, 4])

    resultado = calcular_norma(v)

    assert np.isclose(resultado, 5.0)


def test_similitud_coseno_manual():
    """Compara la similitud coseno contra el cálculo manual."""
    u = np.array([1, 2, 3])
    v = np.array([4, 5, 6])

    esperado = 32 / (np.sqrt(14) * np.sqrt(77))
    resultado = calcular_similitud_coseno(u, v)

    assert np.isclose(resultado, esperado)


def test_diagonal_es_uno():
    """Cada usuario con valoraciones debe tener similitud 1 consigo mismo."""
    matriz = pd.DataFrame(
        [
            [1, 2, 3],
            [4, 5, 6],
        ],
        index=[1, 2],
        columns=[101, 102, 103],
    )

    similitud = calcular_matriz_similitud(matriz)

    assert np.isclose(similitud.loc[1, 1], 1.0)
    assert np.isclose(similitud.loc[2, 2], 1.0)


def test_usuarios_ortogonales():
    """Dos usuarios ortogonales deben tener similitud coseno igual a 0."""
    matriz = pd.DataFrame(
        [
            [1, 0],
            [0, 1],
        ],
        index=[1, 2],
        columns=[101, 102],
    )

    similitud = calcular_matriz_similitud(matriz)

    assert np.isclose(similitud.loc[1, 2], 0.0)
    assert np.isclose(similitud.loc[2, 1], 0.0)


def test_rango_similitud_con_ratings_positivos():
    """Con ratings positivos, las similitudes deben estar entre 0 y 1."""
    matriz = pd.DataFrame(
        [
            [1, 2, 3],
            [3, 4, 5],
            [1, 0, 1],
        ],
        index=[1, 2, 3],
        columns=[101, 102, 103],
    )

    similitud = calcular_matriz_similitud(matriz)

    assert np.all(similitud.values >= 0)
    assert np.all(similitud.values <= 1)


def test_vector_cero_no_rompe_calculo():
    """Un usuario sin valoraciones no debe generar división por cero."""
    matriz = pd.DataFrame(
        [
            [0, 0, 0],
            [1, 2, 3],
        ],
        index=[1, 2],
        columns=[101, 102, 103],
    )

    similitud = calcular_matriz_similitud(matriz)

    assert np.isclose(similitud.loc[1, 1], 0.0)
    assert np.isclose(similitud.loc[1, 2], 0.0)
    assert np.isclose(similitud.loc[2, 1], 0.0)