#src/model/similitud.py

import numpy as np
import pandas as pd


def calcular_producto_punto(u, v):
    """Calcula el producto punto entre dos vectores."""
    u_limpio = np.nan_to_num(u, nan=0.0)
    v_limpio = np.nan_to_num(v, nan=0.0)

    return float(np.dot(u_limpio, v_limpio))


def calcular_norma(v):
    """Calcula la norma euclidiana de un vector."""
    v_limpio = np.nan_to_num(v, nan=0.0)

    return float(np.linalg.norm(v_limpio))


def calcular_similitud_coseno(u, v):
    """Calcula la similitud coseno entre dos vectores."""
    producto_punto = calcular_producto_punto(u, v)
    norma_u = calcular_norma(u)
    norma_v = calcular_norma(v)

    if norma_u == 0 or norma_v == 0:
        return 0.0

    similitud = producto_punto / (norma_u * norma_v)

    return float(np.clip(similitud, -1.0, 1.0))


def obtener_pasos_similitud_coseno(u, v):
    """Retorna los valores intermedios del calculo de similitud coseno."""
    producto_punto = calcular_producto_punto(u, v)
    norma_u = calcular_norma(u)
    norma_v = calcular_norma(v)

    if norma_u == 0 or norma_v == 0:
        similitud = 0.0
    else:
        similitud = producto_punto / (norma_u * norma_v)

    return {
        "producto_punto": float(producto_punto),
        "norma_u": float(norma_u),
        "norma_v": float(norma_v),
        "similitud": float(np.clip(similitud, -1.0, 1.0)),
    }


def calcular_matriz_similitud(matriz):
    """Calcula la matriz de similitud coseno entre usuarios."""
    if not isinstance(matriz, pd.DataFrame):
        raise TypeError("La matriz debe ser un DataFrame de pandas.")

    if matriz.empty:
        raise ValueError("La matriz usuario-pelicula esta vacia.")

    matriz_rellenada = matriz.fillna(0)
    matriz_np = matriz_rellenada.to_numpy(dtype=float)

    productos_punto = np.dot(matriz_np, matriz_np.T)
    normas = np.linalg.norm(matriz_np, axis=1)
    productos_normas = np.outer(normas, normas)

    similitud_np = np.divide(
        productos_punto,
        productos_normas,
        out=np.zeros_like(productos_punto, dtype=float),
        where=productos_normas != 0,
    )

    similitud_np = np.clip(similitud_np, -1.0, 1.0)

    return pd.DataFrame(
        similitud_np,
        index=matriz.index,
        columns=matriz.index,
    )