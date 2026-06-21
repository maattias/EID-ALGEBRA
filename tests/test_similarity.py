import numpy as np

from src.model.similarity import cosine_similarity


def test_diagonal_is_one():
    """
    Cada usuario debe tener similitud 1 consigo mismo.
    """

    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])

    sim = cosine_similarity(matrix)

    assert np.isclose(sim[0, 0], 1.0)
    assert np.isclose(sim[1, 1], 1.0)


def test_orthogonal_users():
    """
    Usuarios ortogonales deben tener similitud 0.
    """

    matrix = np.array([
        [1, 0],
        [0, 1]
    ])

    sim = cosine_similarity(matrix)

    assert np.isclose(sim[0, 1], 0.0)
    assert np.isclose(sim[1, 0], 0.0)


def test_similarity_range():
    """
    Todas las similitudes deben estar entre 0 y 1.
    """

    matrix = np.array([
        [1, 2, 3],
        [3, 4, 5],
        [1, 0, 1]
    ])

    sim = cosine_similarity(matrix)

    assert np.all(sim >= 0)
    assert np.all(sim <= 1)