#ui/styles.py

import streamlit as st

def cargar_estilos() -> None:
    """Carga estilos globales básicos para la aplicación."""
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>

:root {
    --color-fondo: #0F1117;
    --color-superficie: #1C2333;
    --color-borde: #2E3A50;
    --color-primario: #4A90D9;
    --color-texto: #F0F4F8;
    --color-secundario: #A0AEC0;
}

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
    color: var(--color-texto);
}

h1, h2, h3 {
    color: var(--color-texto);
}

[data-testid="stSidebar"] {
    background-color: var(--color-superficie);
    border-right: 1px solid var(--color-borde);
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--color-borde);
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-weight: 500;
    color: var(--color-secundario);
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--color-primario) !important;
    border-bottom: 2px solid var(--color-primario) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--color-borde);
    border-radius: 8px;
    overflow: hidden;
}

[data-testid="stButton"] > button {
    background-color: var(--color-primario);
    color: white;
    border: none;
    border-radius: 8px;
}

hr {
    border-color: var(--color-borde);
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
"""