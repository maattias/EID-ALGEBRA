"""
Autor: Matías

Paleta de colores:
    #0F1117  → fondo oscuro principal   (casi negro azulado)
    #1C2333  → superficies y tarjetas
    #2E3A50  → bordes y separadores
    #4A90D9  → azul primario (acento principal)
    #63B3ED  → azul claro (hover, secundario)
    #F0F4F8  → texto principal
    #A0AEC0  → texto secundario / subtítulos
    #48BB78  → verde para scores altos
    #F6AD55  → naranja para scores medios
    #FC8181  → rojo para scores bajos

Tipografía:
    Display  → 'Space Grotesk' (encabezados, métricas grandes)
    Cuerpo   → 'Inter'         (texto general, párrafos)
    Datos    → monospace nativo (valores numéricos, fórmulas inline)
"""

import streamlit as st


def cargar_estilos() -> None:
    """
    Inyecta el CSS global en la aplicación Streamlit.
    Llamar una sola vez desde app.py antes de renderizar cualquier componente.
    """
    st.markdown(_CSS, unsafe_allow_html=True)


# ── CSS global ─────────────────────────────────────────────────────────────────

_CSS = """
<style>

/* ── Fuentes externas ───────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Variables de color ─────────────────────────────────────────────────── */
:root {
    --color-fondo:        #0F1117;
    --color-superficie:   #1C2333;
    --color-borde:        #2E3A50;
    --color-primario:     #4A90D9;
    --color-primario-light: #63B3ED;
    --color-texto:        #F0F4F8;
    --color-texto-sub:    #A0AEC0;
    --color-verde:        #48BB78;
    --color-naranja:      #F6AD55;
    --color-rojo:         #FC8181;
}

/* ── Tipografía base ────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--color-texto);
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* ── Título principal ───────────────────────────────────────────────────── */
h1 {
    font-size: 2rem;
    color: var(--color-texto);
    margin-bottom: 0.1rem;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--color-superficie);
    border-right: 1px solid var(--color-borde);
}

[data-testid="stSidebar"] h2 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--color-primario-light);
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.75rem;
}

/* ── Tabs ───────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.25rem;
    border-bottom: 1px solid var(--color-borde);
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.875rem;
    color: var(--color-texto-sub);
    padding: 0.5rem 1rem;
    border-radius: 6px 6px 0 0;
    transition: color 0.2s;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--color-primario-light) !important;
    border-bottom: 2px solid var(--color-primario) !important;
    background-color: transparent !important;
}

/* ── Tarjeta de película ────────────────────────────────────────────────── */
.rec-card {
    background-color: var(--color-superficie);
    border: 1px solid var(--color-borde);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.65rem;
    transition: border-color 0.2s, transform 0.15s;
}

.rec-card:hover {
    border-color: var(--color-primario);
    transform: translateX(3px);
}

.rec-card-titulo {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--color-texto);
    margin-bottom: 0.3rem;
}

.rec-card-meta {
    font-size: 0.78rem;
    color: var(--color-texto-sub);
}

/* ── Badge de score ─────────────────────────────────────────────────────── */
.badge-score {
    display: inline-block;
    font-family: monospace;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
    margin-left: 0.5rem;
}

.badge-alto   { background-color: #1a3a2a; color: var(--color-verde); }
.badge-medio  { background-color: #3a2a10; color: var(--color-naranja); }
.badge-bajo   { background-color: #3a1a1a; color: var(--color-rojo); }

/* ── Métrica destacada ──────────────────────────────────────────────────── */
.metrica-box {
    background-color: var(--color-superficie);
    border: 1px solid var(--color-borde);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.metrica-valor {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-primario-light);
    line-height: 1;
}

.metrica-label {
    font-size: 0.75rem;
    color: var(--color-texto-sub);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.35rem;
}

/* ── Sección matemática ─────────────────────────────────────────────────── */
.formula-box {
    background-color: var(--color-superficie);
    border-left: 3px solid var(--color-primario);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    font-family: monospace;
}

.paso-box {
    background-color: #111827;
    border: 1px solid var(--color-borde);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 0;
    font-size: 0.875rem;
}

.paso-numero {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    color: var(--color-primario);
    margin-right: 0.5rem;
}

/* ── Tabla interactiva ──────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--color-borde);
    border-radius: 8px;
    overflow: hidden;
}

/* ── Botones ────────────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    background-color: var(--color-primario);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    padding: 0.45rem 1.2rem;
    transition: background-color 0.2s;
}

[data-testid="stButton"] > button:hover {
    background-color: var(--color-primario-light);
    color: var(--color-fondo);
}

/* ── Sliders ────────────────────────────────────────────────────────────── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: var(--color-primario) !important;
}

/* ── Selectbox ──────────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background-color: var(--color-superficie);
    border: 1px solid var(--color-borde);
    border-radius: 8px;
    color: var(--color-texto);
}

/* ── Divider ────────────────────────────────────────────────────────────── */
hr {
    border-color: var(--color-borde);
    margin: 1.5rem 0;
}

/* ── Mensajes de estado ─────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
}

/* ── Ocultar elementos de Streamlit que no necesitamos ──────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

</style>
"""