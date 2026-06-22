#ui/components.py

import pandas as pd
import streamlit as st


def mensaje_vacio(mensaje: str, sugerencia: str = "") -> None:
    """Muestra un mensaje cuando no existen datos para mostrar."""
    st.info(mensaje)

    if sugerencia:
        st.caption(sugerencia)


def tabla_similitud(similitudes: pd.Series) -> None:
    """Muestra una tabla simple con usuarios similares y similitud coseno."""
    if similitudes.empty:
        mensaje_vacio("No se encontraron usuarios similares.")
        return

    tabla = similitudes.reset_index()
    tabla.columns = ["Usuario", "Similitud coseno"]
    tabla["Similitud coseno"] = tabla["Similitud coseno"].round(4)

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
    )


def mostrar_metrica(columna, etiqueta: str, valor) -> None:
    """Muestra una métrica dentro de una columna de Streamlit."""
    columna.metric(etiqueta, valor)