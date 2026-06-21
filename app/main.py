# app/main.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from components import (
    movie_card,
    similarity_table,
    user_profile_section
)

# ==================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Sistema de Recomendación",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Sistema de Recomendación de Películas")

# ==================================================
# DATOS DE EJEMPLO
# (Luego serán reemplazados por el recomendador real)
# ==================================================

users = [1, 2, 3, 4, 5]

all_genres = [
    "Acción",
    "Comedia",
    "Drama",
    "Sci-Fi",
    "Terror",
    "Romance"
]

recommendations = [
    {
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "score": 4.92
    },
    {
        "title": "The Dark Knight",
        "genre": "Acción",
        "score": 4.88
    },
    {
        "title": "Inception",
        "genre": "Sci-Fi",
        "score": 4.81
    },
    {
        "title": "Titanic",
        "genre": "Romance",
        "score": 4.55
    }
]

rated_movies = [
    "Avatar",
    "Toy Story",
    "Matrix",
    "Titanic"
]

# ==================================================
# MATRIZ DE SIMILITUD FICTICIA
# ==================================================

similarity_matrix = pd.DataFrame(
    [
        [1.00, 0.85, 0.42, 0.31, 0.70],
        [0.85, 1.00, 0.38, 0.27, 0.66],
        [0.42, 0.38, 1.00, 0.74, 0.51],
        [0.31, 0.27, 0.74, 1.00, 0.48],
        [0.70, 0.66, 0.51, 0.48, 1.00]
    ],
    index=users,
    columns=users
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("⚙️ Configuración")

selected_user = st.sidebar.selectbox(
    "Seleccionar usuario",
    users
)

favorite_genres = st.sidebar.multiselect(
    "Géneros favoritos",
    all_genres,
    default=["Sci-Fi"]
)

k = st.sidebar.slider(
    "Número de vecinos (K)",
    min_value=1,
    max_value=20,
    value=5
)

n = st.sidebar.slider(
    "Número de recomendaciones (N)",
    min_value=1,
    max_value=20,
    value=5
)

# ==================================================
# PESTAÑAS
# ==================================================

tab1, tab2 = st.tabs(
    ["🎯 Recomendaciones", "📊 Análisis"]
)

# ==================================================
# TAB RECOMENDACIONES
# ==================================================

with tab1:

    st.header("Mi Perfil")

    densidad = len(rated_movies) / 20

    user_profile_section(
        selected_user,
        rated_movies,
        favorite_genres
    )

    st.metric(
        "Densidad del vector",
        f"{densidad:.2%}"
    )

    st.divider()

    st.header("Películas Recomendadas")

    recommendations_sorted = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    for movie in recommendations_sorted[:n]:

        movie_card(
            movie["title"],
            movie["genre"],
            movie["score"]
        )

# ==================================================
# TAB ANÁLISIS
# ==================================================

with tab2:

    st.header("Mapa de Calor de Similitud")

    fig, ax = plt.subplots(figsize=(6, 5))

    heatmap = ax.imshow(
        similarity_matrix,
        aspect="auto"
    )

    ax.set_xticks(range(len(users)))
    ax.set_yticks(range(len(users)))

    ax.set_xticklabels(users)
    ax.set_yticklabels(users)

    plt.colorbar(
        heatmap,
        ax=ax
    )

    st.pyplot(fig)

    st.divider()

    similarity_table(similarity_matrix)