#ui/tabs/tab_matematicas.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.model.similarity import obtener_pasos_similitud_coseno


def render_tab_matematicas():
    """Muestra la base matematica del sistema de recomendacion."""
    st.header("Fundamentos matematicos")

    st.subheader("Matriz usuario-pelicula")
    st.write(
        "Las preferencias se representan mediante una matriz donde cada fila es un "
        "usuario, cada columna es una pelicula y cada celda contiene una valoracion."
    )

    matriz_ejemplo = pd.DataFrame(
        {
            "Pelicula A": [5.0, 4.0, 1.0],
            "Pelicula B": [4.0, 5.0, 2.0],
            "Pelicula C": [0.0, 3.0, 5.0],
        },
        index=["Usuario 1", "Usuario 2", "Usuario 3"],
    )

    matriz_editada = st.data_editor(
        matriz_ejemplo,
        use_container_width=True,
        num_rows="fixed",
    )

    st.write(
        "En este ejemplo, el valor 0 representa una pelicula no valorada. "
        "La matriz permite tratar a cada usuario como un vector numerico."
    )

    st.divider()

    st.subheader("Similitud coseno")

    st.write(
        "La similitud coseno compara la direccion de dos vectores. "
        "En recomendacion, permite medir que tan parecidos son dos usuarios "
        "segun sus patrones de valoracion."
    )

    st.latex(
        r"""
        \cos(\theta)=
        \frac{\mathbf{u}\cdot\mathbf{v}}
        {\|\mathbf{u}\|\|\mathbf{v}\|}
        """
    )

    usuarios = list(matriz_editada.index)

    col1, col2 = st.columns(2)

    with col1:
        usuario_a = st.selectbox("Primer usuario", usuarios, index=0)

    with col2:
        usuario_b = st.selectbox("Segundo usuario", usuarios, index=1)

    vector_u = matriz_editada.loc[usuario_a].to_numpy(dtype=float)
    vector_v = matriz_editada.loc[usuario_b].to_numpy(dtype=float)

    pasos = obtener_pasos_similitud_coseno(vector_u, vector_v)

    producto_punto = pasos["producto_punto"]
    norma_u = pasos["norma_u"]
    norma_v = pasos["norma_v"]
    similitud = pasos["similitud"]

    st.subheader("Calculo paso a paso")

    st.write(f"Vector de {usuario_a}: `{vector_u}`")
    st.write(f"Vector de {usuario_b}: `{vector_v}`")

    st.latex(
        rf"""
        \mathbf{{u}}\cdot\mathbf{{v}} = {producto_punto:.2f}
        """
    )

    st.latex(
        rf"""
        \|\mathbf{{u}}\| = {norma_u:.4f}
        """
    )

    st.latex(
        rf"""
        \|\mathbf{{v}}\| = {norma_v:.4f}
        """
    )

    st.latex(
        rf"""
        \cos(\theta) =
        \frac{{{producto_punto:.2f}}}
        {{{norma_u:.4f}\times{norma_v:.4f}}}
        =
        {similitud:.4f}
        """
    )

    st.metric(
        label=f"Similitud entre {usuario_a} y {usuario_b}",
        value=f"{similitud:.4f}",
    )

    if similitud >= 0.8:
        st.success("Alta similitud: los usuarios tienen preferencias muy parecidas.")
    elif similitud >= 0.5:
        st.info("Similitud media: los usuarios comparten algunos patrones de gusto.")
    else:
        st.warning("Baja similitud: los usuarios tienen patrones poco relacionados.")

    st.divider()

    st.subheader("Visualizacion vectorial en 2D")

    columnas = list(matriz_editada.columns)

    vector_u_2d = vector_u[:2]
    vector_v_2d = vector_v[:2]

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.quiver(
        0,
        0,
        vector_u_2d[0],
        vector_u_2d[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        label=usuario_a,
    )

    ax.quiver(
        0,
        0,
        vector_v_2d[0],
        vector_v_2d[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        label=usuario_b,
    )

    maximo = max(
        float(np.max(vector_u_2d)),
        float(np.max(vector_v_2d)),
        1.0,
    )

    ax.set_xlim(0, maximo + 1)
    ax.set_ylim(0, maximo + 1)
    ax.set_xlabel(columnas[0])
    ax.set_ylabel(columnas[1])
    ax.set_title("Vectores de usuarios en dos dimensiones")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.write(
        "Mientras menor sea el angulo entre los vectores, mayor sera la similitud. "
        "Por eso, usuarios con vectores apuntando en una direccion parecida pueden "
        "servir como referencia para generar recomendaciones."
    )

    st.divider()

    st.subheader("Recomendación logica con matriz pequeña")

    peliculas_no_vistas = [
        columna
        for columna in columnas
        if matriz_editada.at[usuario_a, columna] == 0
    ]

    if usuario_a == usuario_b:
        st.warning("Selecciona dos usuarios distintos para generar una recomendacion.")
        return

    if not peliculas_no_vistas:
        st.info(f"{usuario_a} ya tiene valoraciones en todas las peliculas del ejemplo.")
        return

    candidatas = {
        pelicula: matriz_editada.at[usuario_b, pelicula]
        for pelicula in peliculas_no_vistas
        if matriz_editada.at[usuario_b, pelicula] > 0
    }

    if not candidatas:
        st.info(
            f"{usuario_b} no ha valorado las peliculas faltantes de {usuario_a}, "
            "por lo que no hay suficiente informacion para recomendar."
        )
        return

    pelicula_recomendada = max(candidatas, key=candidatas.get)
    puntaje_referencia = candidatas[pelicula_recomendada]

    st.write(
        f"{usuario_a} no ha valorado: {peliculas_no_vistas}. "
        f"{usuario_b} si valoro algunas de esas peliculas. "
        f"La mejor candidata es {pelicula_recomendada}, con rating {puntaje_referencia}."
    )

    if similitud >= 0.5:
        st.success(
            f"Se recomienda {pelicula_recomendada} porque {usuario_a} y {usuario_b} "
            f"presentan una similitud coseno de {similitud:.4f}."
        )
    else:
        st.warning(
            f"{pelicula_recomendada} podria recomendarse, pero la confianza es baja "
            f"porque la similitud coseno es {similitud:.4f}."
        )