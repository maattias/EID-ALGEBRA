"""
Autor: Matías

Componentes disponibles:
    tarjeta_pelicula()   → tarjeta con título, score y nº de vecinos que valoraron
    badge_score()        → badge de color según rango de score (alto/medio/bajo)
    metrica_destacada()  → caja de métrica grande con valor y etiqueta
    separador_seccion()  → título de sección con línea decorativa
    mensaje_vacio()      → estado vacío cuando no hay resultados
    tabla_similitud()    → tabla formateada de usuarios similares
"""

import streamlit as st
import pandas as pd


# ── Tarjeta de película recomendada ───────────────────────────────────────────

def tarjeta_pelicula(
    titulo: str,
    score: float,
    n_vecinos: int,
    posicion: int,
) -> None:
    """
    Renderiza una tarjeta con la información de una película recomendada.

    Parámetros
    ----------
    titulo    : str   — nombre de la película
    score     : float — score predicho por el sistema (0.0 – 5.0)
    n_vecinos : int   — cuántos vecinos valoraron esta película
    posicion  : int   — número de posición en el ranking (1, 2, 3...)
    """
    clase_badge = _clase_badge(score)
    estrellas   = _score_a_estrellas(score)

    st.markdown(
        f"""
        <div class="rec-card">
            <div class="rec-card-titulo">
                <span style="color: #4A90D9; font-size: 0.8rem; margin-right: 0.5rem;">
                    #{posicion}
                </span>
                {titulo}
                <span class="badge-score {clase_badge}">{score:.2f}</span>
            </div>
            <div class="rec-card-meta">
                {estrellas} &nbsp;·&nbsp;
                Valorada por <b>{n_vecinos}</b> usuario{'s' if n_vecinos != 1 else ''} similar{'es' if n_vecinos != 1 else ''}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Badge de score ─────────────────────────────────────────────────────────────

def badge_score(score: float) -> str:
    """
    Retorna el HTML de un badge de color según el rango del score.
    Para usar dentro de otros componentes HTML.

    Parámetros
    ----------
    score : float — valor entre 0.0 y 5.0

    Retorna
    -------
    str — HTML del badge
    """
    clase = _clase_badge(score)
    return f'<span class="badge-score {clase}">{score:.2f}</span>'


# ── Métrica destacada ──────────────────────────────────────────────────────────

def metrica_destacada(valor: str, etiqueta: str, col=None) -> None:
    """
    Renderiza una caja de métrica con valor grande y etiqueta pequeña.

    Parámetros
    ----------
    valor    : str       — valor a mostrar (ya formateado, e.g. "1,682")
    etiqueta : str       — descripción del valor (e.g. "Usuarios totales")
    col      : contexto de columna Streamlit (opcional, si None usa el contexto actual)
    """
    html = f"""
    <div class="metrica-box">
        <div class="metrica-valor">{valor}</div>
        <div class="metrica-label">{etiqueta}</div>
    </div>
    """
    ctx = col if col is not None else st
    ctx.markdown(html, unsafe_allow_html=True)


# ── Separador de sección ───────────────────────────────────────────────────────

def separador_seccion(titulo: str, descripcion: str = "") -> None:
    """
    Renderiza un encabezado de sección con título y descripción opcional.

    Parámetros
    ----------
    titulo      : str — título de la sección
    descripcion : str — subtítulo o descripción breve (opcional)
    """
    st.markdown(f"### {titulo}")
    if descripcion:
        st.caption(descripcion)


# ── Estado vacío ───────────────────────────────────────────────────────────────

def mensaje_vacio(mensaje: str, sugerencia: str = "") -> None:
    """
    Muestra un estado vacío cuando no hay resultados que mostrar.

    Parámetros
    ----------
    mensaje    : str — mensaje principal
    sugerencia : str — qué puede hacer el usuario para obtener resultados
    """
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: 2.5rem 1rem;
            color: #A0AEC0;
            border: 1px dashed #2E3A50;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <div style="font-weight: 500; margin-bottom: 0.3rem;">{mensaje}</div>
            <div style="font-size: 0.8rem;">{sugerencia}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Tabla de usuarios similares ────────────────────────────────────────────────

def tabla_similitud(
    similitudes: pd.Series,
    user_id_objetivo: int,
) -> None:
    """
    Renderiza una tabla formateada con los usuarios más similares
    al usuario objetivo y sus scores de similitud.

    Parámetros
    ----------
    similitudes      : pd.Series — índice = userId, valores = similitud coseno
    user_id_objetivo : int       — ID del usuario objetivo (para contexto)
    """
    if similitudes.empty:
        mensaje_vacio(
            "No se encontraron usuarios similares.",
            "Prueba ajustando el número de vecinos en el sidebar.",
        )
        return

    df_tabla = similitudes.reset_index()
    df_tabla.columns = ["Usuario", "Similitud coseno"]
    df_tabla.index   = df_tabla.index + 1   # ranking desde 1

    # Formatear la columna de similitud con barra de progreso visual
    df_tabla["Similitud coseno"] = df_tabla["Similitud coseno"].round(4)

    st.dataframe(
        df_tabla,
        use_container_width=True,
        column_config={
            "Usuario": st.column_config.NumberColumn(
                "Usuario ID",
                help="Identificador del usuario vecino",
            ),
            "Similitud coseno": st.column_config.ProgressColumn(
                "Similitud coseno",
                help="Valor de similitud coseno respecto al usuario objetivo (0 a 1)",
                format="%.4f",
                min_value=0.0,
                max_value=1.0,
            ),
        },
        hide_index=False,
    )


# ── Helpers internos ───────────────────────────────────────────────────────────

def _clase_badge(score: float) -> str:
    """Retorna la clase CSS del badge según el rango del score."""
    if score >= 4.0:
        return "badge-alto"
    elif score >= 3.0:
        return "badge-medio"
    else:
        return "badge-bajo"


def _score_a_estrellas(score: float) -> str:
    """Convierte un score numérico a representación con emojis de estrella."""
    llenas  = int(round(score))
    llenas  = max(0, min(5, llenas))
    vacias  = 5 - llenas
    return "⭐" * llenas + "☆" * vacias