import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def _get_user_item_matrix():
    for key in ["user_item_matrix", "matrix", "ratings_matrix"]:
        value = st.session_state.get(key)
        if isinstance(value, pd.DataFrame):
            return value
    return None


def _get_similarity_matrix(user_item_matrix):
    for key in ["similarity_matrix", "sim_matrix", "user_similarity"]:
        value = st.session_state.get(key)

        if isinstance(value, pd.DataFrame):
            return value

        if isinstance(value, np.ndarray):
            return pd.DataFrame(
                value,
                index=user_item_matrix.index,
                columns=user_item_matrix.index
            )

    filled = user_item_matrix.fillna(0).to_numpy(dtype=float)
    norms = np.linalg.norm(filled, axis=1)

    denominator = np.outer(norms, norms)
    numerator = filled @ filled.T

    with np.errstate(divide="ignore", invalid="ignore"):
        similarity = numerator / denominator
        similarity[np.isnan(similarity)] = 0

    return pd.DataFrame(
        similarity,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )


def _get_selected_user(similarity_df):
    selected = st.session_state.get("selected_user")

    if selected in similarity_df.index:
        return selected

    try:
        selected_int = int(selected)
        if selected_int in similarity_df.index:
            return selected_int
    except (TypeError, ValueError):
        pass

    return similarity_df.index[0]


def _plot_heatmap(similarity_df, sample_size):
    sample_size = min(sample_size, len(similarity_df))
    sample = similarity_df.iloc[:sample_size, :sample_size]

    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(sample.values, aspect="auto")

    ax.set_title("Mapa de calor de similitud entre usuarios")
    ax.set_xlabel("Usuarios")
    ax.set_ylabel("Usuarios")

    ax.set_xticks(range(len(sample.columns)))
    ax.set_xticklabels(sample.columns, rotation=90, fontsize=8)

    ax.set_yticks(range(len(sample.index)))
    ax.set_yticklabels(sample.index, fontsize=8)

    fig.colorbar(image, ax=ax, label="Similitud coseno")
    st.pyplot(fig)
    plt.close(fig)


def _show_top_similar_users(similarity_df, selected_user):
    scores = similarity_df.loc[selected_user].drop(index=selected_user, errors="ignore")
    top_users = scores.sort_values(ascending=False).head(5)

    result = pd.DataFrame({
        "Usuario similar": top_users.index,
        "Score de similitud": top_users.values
    })

    st.dataframe(result, use_container_width=True)


def _plot_profile_comparison(user_item_matrix, similarity_df, selected_user):
    """
    Compara el perfil de ratings del usuario objetivo contra su vecino más cercano.
    """

    scores = similarity_df.loc[selected_user].drop(index=selected_user, errors="ignore")

    if scores.empty:
        st.info("No hay vecinos disponibles para comparar.")
        return

    nearest_user = scores.sort_values(ascending=False).index[0]

    selected_ratings = user_item_matrix.loc[selected_user]
    neighbor_ratings = user_item_matrix.loc[nearest_user]

    common_items = selected_ratings.notna() & neighbor_ratings.notna()

    comparison = pd.DataFrame({
        f"Usuario {selected_user}": selected_ratings[common_items],
        f"Vecino {nearest_user}": neighbor_ratings[common_items],
    })

    if comparison.empty:
        st.info(
            f"El usuario {selected_user} y el vecino {nearest_user} no tienen películas valoradas en común."
        )
        return

    comparison["Diferencia"] = (
        comparison[f"Usuario {selected_user}"] - comparison[f"Vecino {nearest_user}"]
    ).abs()

    comparison = comparison.sort_values("Diferencia").head(12)
    comparison = comparison.drop(columns=["Diferencia"])

    fig, ax = plt.subplots(figsize=(9, 5))
    comparison.plot(kind="bar", ax=ax)

    ax.set_title(
        f"Películas valoradas por ambos: usuario {selected_user} vs vecino {nearest_user}"
    )
    ax.set_xlabel("Películas")
    ax.set_ylabel("Rating")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


def render_tab_similitud():
    st.header("Análisis de similitud entre usuarios")

    user_item_matrix = _get_user_item_matrix()

    if user_item_matrix is None or user_item_matrix.empty:
        st.error("No existe `user_item_matrix` en `st.session_state`.")
        return

    similarity_df = _get_similarity_matrix(user_item_matrix)
    selected_user = _get_selected_user(similarity_df)
    sample_size = int(st.session_state.get("sample_size", 20))

    st.subheader("Mapa de calor de similitud")
    _plot_heatmap(similarity_df, sample_size)

    st.subheader(f"Top 5 usuarios más similares al usuario {selected_user}")
    _show_top_similar_users(similarity_df, selected_user)

    st.subheader("Comparación de perfiles de rating")
    _plot_profile_comparison(user_item_matrix, similarity_df, selected_user)


render = render_tab_similitud