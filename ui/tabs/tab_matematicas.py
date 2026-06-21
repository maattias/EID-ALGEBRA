import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.similarity import get_cosine_similarity_steps


def mostrar_tab_matematicas():
    st.header("Fundamentos Matemáticos")

    # =====================================================
    # INTRODUCCIÓN
    # =====================================================
    st.subheader("¿Qué es un Sistema de Recomendación?")

    st.write("""
    Los sistemas de recomendación son herramientas utilizadas por plataformas digitales 
    para sugerir contenido personalizado a los usuarios. Actualmente son empleados en 
    servicios como Netflix, Spotify, YouTube y Amazon para recomendar películas, 
    canciones, libros o productos según los intereses y preferencias de cada persona.
    
    Estos sistemas analizan las valoraciones e interacciones de los usuarios y utilizan 
    técnicas matemáticas para identificar patrones de comportamiento y similitudes entre 
    perfiles.
    """)

    # =====================================================
    # SIMILITUD COSENO
    # =====================================================
    st.subheader("Similitud Coseno")

    st.write("""
    Una de las métricas más utilizadas en sistemas de recomendación es la similitud coseno. 
    Esta medida permite comparar dos vectores y determinar qué tan parecidas son sus 
    preferencias, midiendo el ángulo entre ellos independientemente de su magnitud.
    """)

    st.latex(r"""
    \cos(\theta)=
    \frac{\mathbf{u}\cdot\mathbf{v}}
    {\|\mathbf{u}\|\|\mathbf{v}\|}
    """)

    st.write("""
    Donde:
    - **u** y **v** representan dos usuarios o productos.
    - **u · v** corresponde al producto punto.
    - **||u||** y **||v||** representan la magnitud (o norma euclidiana) de cada vector.
    
    Si el valor obtenido es cercano a 1, significa que ambos usuarios poseen gustos 
    similares y pueden utilizarse para generar recomendaciones.
    """)

    # =====================================================
    # MATRIZ INTERACTIVA
    # =====================================================
    st.subheader("Ejemplo Interactivo: Matriz Usuario-Película")

    st.write("""
    La siguiente matriz representa las valoraciones de tres usuarios sobre tres películas. 
    Puede modificar libremente los valores directamente en la tabla para observar distintos escenarios.
    """)

    matriz_inicial = pd.DataFrame(
        {
            "Película A": [5.0, 4.0, 1.0],
            "Película B": [4.0, 5.0, 2.0],
            "Película C": [0.0, 3.0, 5.0],
        },
        index=["Usuario 1", "Usuario 2", "Usuario 3"]
    )

    matriz_editada = st.data_editor(
        matriz_inicial,
        use_container_width=True,
        num_rows="fixed"
    )

    st.info("""
    💡 **Nota de interpretación:** Cada fila representa un usuario y cada columna una película. 
    Los valores corresponden a las calificaciones otorgadas. 
    Un valor 0 indica que el usuario aún no ha valorado esa película (dato faltante).
    """)

    # =====================================================
    # CÁLCULO PASO A PASO
    # =====================================================
    st.subheader("Cálculo Paso a Paso de la Similitud Coseno")

    usuarios = list(matriz_editada.index)
    columnas_peliculas = list(matriz_editada.columns)

    col1, col2 = st.columns(2)
    with col1:
        usuario_a = st.selectbox("Primer usuario", usuarios, index=0)
    with col2:
        usuario_b = st.selectbox("Segundo usuario", usuarios, index=1)

    vector_u = matriz_editada.loc[usuario_a].values.astype(float)
    vector_v = matriz_editada.loc[usuario_b].values.astype(float)

    st.write("### Vectores seleccionados")
    st.write(f"**{usuario_a} ($\mathbf{{u}}$):** {vector_u}")
    st.write(f"**{usuario_b} ($\mathbf{{v}}$):** {vector_v}")

    pasos = get_cosine_similarity_steps(vector_u, vector_v)
    
    # Extraemos los valores del diccionario de Gustavo para no romper el resto de tu código
    producto_punto = pasos["producto_punto"]
    norma_u = pasos["norma_u"]
    norma_v = pasos["norma_v"]
    similitud = pasos["similitud"]

    st.write("### 4. Resultado de Similitud Coseno")
    st.latex(rf"""
    \cos(\theta) = \frac{{{producto_punto:.2f}}}{{{norma_u:.4f} \times {norma_v:.4f}}} = {similitud:.4f}
    """)

    st.metric(label=f"Similitud entre {usuario_a} y {usuario_b}", value=f"{similitud:.4f}")

    # Interpretación analítica
    st.write("### Interpretación del Resultado")
    if similitud > 0.8:
        st.success(f"🎯 **Alta similitud:** Los usuarios presentan gustos muy alineados. Es altamente viable usar las películas preferidas de uno para recomendárselas al otro.")
    elif similitud > 0.5:
        st.info(f"📊 **Similitud moderada:** Tienen ciertas preferencias en común, pero también marcadas diferencias.")
    else:
        st.warning(f"⚠️ **Baja similitud:** Los vectores apuntan en direcciones muy distintas. Sus gustos no guardan relación estrecha.")

    # =====================================================
    # VISUALIZACIÓN GEOMÉTRICA
    # =====================================================
    st.subheader("Visualización Geométrica de los Vectores")

    st.write(f"""
    Para efectos prácticos de visualización en un plano 2D, se toman únicamente las dos primeras 
    columnas disponibles de la matriz (**{columnas_peliculas[0]}** y **{columnas_peliculas[1]}**). 
    Geométricamente, la similitud coseno equivale al coseno del ángulo $\\theta$ formado por estos vectores.
    """)

    # Reducción 2D usando las 2 primeras columnas dinámicas
    vector_u_2d = vector_u[:2]
    vector_v_2d = vector_v[:2]

    # Cálculos para el espacio 2D con protección contra división por cero
    producto_2d = np.dot(vector_u_2d, vector_v_2d)
    norma_u_2d = np.linalg.norm(vector_u_2d)
    norma_v_2d = np.linalg.norm(vector_v_2d)

    if norma_u_2d > 0 and norma_v_2d > 0:
        cos_theta = np.clip(producto_2d / (norma_u_2d * norma_v_2d), -1.0, 1.0)
        angulo = np.degrees(np.arccos(cos_theta))
    else:
        angulo = 0.0

    # Renderizado seguro del gráfico Matplotlib
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Dibujar vectores usando quiver de forma explícita y con color contrastante
    ax.quiver(0, 0, vector_u_2d[0], vector_u_2d[1], angles='xy', scale_units='xy', scale=1, color='#1E88E5', label=usuario_a)
    ax.quiver(0, 0, vector_v_2d[0], vector_v_2d[1], angles='xy', scale_units='xy', scale=1, color='#D81B60', label=usuario_b)

    # Establecer límites dinámicos basándose en los datos para evitar que los vectores se corten
    max_val = max(np.max(vector_u_2d), np.max(vector_v_2d), 1) + 1
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)

    # Etiquetas dinámicas basadas en los nombres reales de las columnas
    ax.set_xlabel(columnas_peliculas[0])
    ax.set_ylabel(columnas_peliculas[1])
    ax.set_title("Espacio Vectorial 2D (Primeras 2 Películas)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Enviar gráfico a Streamlit de manera limpia
    st.pyplot(fig)

    # Resultados geométricos finales
    st.write("### Resultados Geométricos")
    st.latex(rf"\theta = {angulo:.2f}^\circ")
    st.write(f"Ángulo calculado en 2D: **{angulo:.2f}°**")

    if angulo < 25:
        st.success("📐 Los vectores se encuentran muy juntos en el espacio (ángulo cerrado). Esto ratifica una gran afinidad en sus gustos de forma visual.")
    elif angulo < 50:
        st.info("📐 Los vectores muestran una apertura intermedia, reflejando coincidencias parciales.")
    else:
        st.warning("📐 Apertura angular pronunciada. Gráficamente se evidencia que los perfiles difieren de manera importante.")

    # =====================================================
    # GENERACIÓN DE RECOMENDACIÓN LÓGICA 
    # =====================================================
    st.write("---")
    st.subheader("Generación de una Recomendación Lógica")

    st.write(f"""
    Utilizando los resultados del cálculo matemático, podemos aplicar un principio de 
    **Filtrado Colaborativo** para predecir qué contenido le podría gustar a **{usuario_a}** tomando como referencia a **{usuario_b}**.
    """)

    # Identificar índices de las películas que el Usuario A no ha visto (valor == 0)
    peliculas_no_vistas_a = [col for col in columnas_peliculas if matriz_editada.at[usuario_a, col] == 0]
    
    st.write("#### 🔎 Análisis de afinidad paso a paso:")

    # Caso 1: Los usuarios son el mismo
    if usuario_a == usuario_b:
        st.warning(f"Por favor, selecciona dos usuarios **diferentes** en los selectores de arriba para poder realizar una recomendación cruzada.")
    
    # Caso 2: El usuario objetivo ya vio todo, no hay nada que recomendar
    elif len(peliculas_no_vistas_a) == 0:
        st.info(f"**Paso 1:** Analizando el perfil de **{usuario_a}**... Se observa que ya ha calificado todas las películas disponibles en esta matriz pequeña. No existen vacíos de información para recomendar.")
    
    else:
        st.write(f"1. **Identificar vacíos:** Analizamos qué películas **{usuario_a}** aún no ha visto (calificación igual a 0). Encontramos: `{peliculas_no_vistas_a}`.")
        st.write(f"2. **Evaluar el puente de similitud:** El grado de coincidencia actual entre ambos perfiles es de **{similitud:.4f}**.")
        
        # CORREGIDO: Uso de llaves simples para la comprensión del diccionario de candidatas
        candidatas = {col: matriz_editada.at[usuario_b, col] for col in peliculas_no_vistas_a if matriz_editada.at[usuario_b, col] > 0}
        
        if len(candidatas) == 0:
            st.error(f"3. **Resultado:** Aunque **{usuario_a}** no ha visto algunas películas, **{usuario_b}** tampoco las ha calificado. No hay suficiente información compartida para generar una recomendación directa.")
        else:
            # Seleccionar la película con mayor puntaje del usuario B
            pelicula_recomendada = max(candidatas, key=candidatas.get)
            puntaje_b = candidatas[pelicula_recomendada]
            
            st.write(f"3. **Buscar el mayor interés de {usuario_b}:** Evaluamos las calificaciones de {usuario_b} en esos vacíos: {candidatas}.")
            
            # Justificación final según el umbral de similitud
            st.write("#### 🎯 Justificación e Impacto Ingenieril:")
            
            if similitud > 0.5:
                st.success(f"""
                **¡Recomendación Exitosa!** Se le recomienda a **{usuario_a}** ver **"{pelicula_recomendada}"**.
                
                **Justificación:** Dado que **{usuario_a}** y **{usuario_b}** tienen gustos similares (Similitud Coseno de ${similitud:.4f}$), el sistema asume matemáticamente que compartirán opiniones futuras. Como **{usuario_b}** calificó **"{pelicula_recomendada}"** con una puntuación destacada de **{puntaje_b}**, existe una alta probabilidad de que sea del agrado de **{usuario_a}**.
                """)
            else:
                st.warning(f"""
                **Recomendación con Reserva (Baja Confianza):** El sistema sugiere **"{pelicula_recomendada}"** por ser el contenido con mayor puntaje de {usuario_b} ({puntaje_b}), **pero el nivel de confianza es bajo**.
                
                **Justificación:** El índice de similitud coseno es de apenas ${similitud:.4f}$. Al no estar alineados sus vectores de preferencia, el comportamiento de **{usuario_b}** no es un predictor confiable para **{usuario_a}**. En la práctica de la ingeniería de software, este resultado se descartaría o se penalizaría por falta de correlación.
                """)

    # =====================================================
    # COMPARACIÓN DE MÉTRICAS
    # =====================================================
    st.write("---")
    st.subheader("Comparación de Métricas: Coseno vs. Distancia Euclidiana")

    st.write(f"""
    En el diseño de sistemas de recomendación, la elección de la métrica de afinidad es crucial. 
    A continuación, se calcula en paralelo la **Similitud Coseno** y la **Distancia Euclidiana** para los vectores de **{usuario_a}** y **{usuario_b}** usando la matriz completa (3D) para analizar sus diferencias.
    """)

    # Cálculo de Distancia Euclidiana
    # d = sqrt( sum( (u_i - v_i)^2 ) )
    diferencia_vectores = vector_u - vector_v
    suma_cuadrados_dif = np.sum(diferencia_vectores ** 2)
    distancia_euclidiana = np.linalg.norm(diferencia_vectores)

    # Crear dos columnas para mostrar las métricas en paralelo
    met_col1, met_col2 = st.columns(2)

    with met_col1:
        st.info("###📐 Similitud Coseno")
        st.latex(r"\cos(\theta) = \frac{\mathbf{u}\cdot\mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}")
        st.metric(label="Resultado Coseno", value=f"{similitud:.4f}")
        st.write("""
        - **Rango:** [-1, 1] (En calificaciones positivas suele estar entre 0 y 1).
        - **Interpretación:** Cercano a 1 indica máxima similitud de tendencias.
        - **Naturaleza:** Mide la **dirección** y el ángulo, ignorando la magnitud de las notas.
        """)

    with met_col2:
        st.warning("### 📏 Distancia Euclidiana")
        st.latex(rf"d(\mathbf{{u}}, \mathbf{{v}}) = \sqrt{{\sum (u_i - v_i)^2}}")
        st.metric(label="Resultado Euclidiano", value=f"{distancia_euclidiana:.4f}")
        st.write("""
        - **Rango:** [0, $+\infty$).
        - **Interpretación:** Cercano a 0 indica que los perfiles están muy cerca.
        - **Naturaleza:** Mide la **distancia física en línea recta** entre los puntos.
        """)

    # Desglose matemático de la distancia euclidiana
    st.write("#### Desarrollo paso a paso de la Distancia Euclidiana:")
    terminos_euclidianos = " + ".join([f"({u} - {v})^2" for u, v in zip(vector_u, vector_v)])
    valores_euclidianos = " + ".join([f"({u-v:.1f})^2" for u, v in zip(vector_u, vector_v)])
    st.latex(rf"d = \sqrt{{{terminos_euclidianos}}}")
    st.latex(rf"d = \sqrt{{{valores_euclidianos}}} = \sqrt{{{suma_cuadrados_dif:.2f}}} = {distancia_euclidiana:.4f}")

    # Análisis Crítico e Discusión (Exigencia de enfoque ingenieril del PDF)
    st.write("#### 🧠 Discusión Crítica e Impacto en Sistemas de Recomendación")
    
    st.write(f"""
    Al observar los datos dinámicos de **{usuario_a}** y **{usuario_b}**, podemos extraer conclusiones metodológicas importantes:
    
    1. **El efecto de la escala y severidad:** Si modificas la matriz interactiva de arriba de modo que el *Usuario 1* tenga notas `[5, 4, 1]` y el *Usuario 2* tenga notas proporcionalmente más bajas pero con la misma tendencia como `[2.5, 2, 0.5]`, notarás que la **Similitud Coseno se mantiene en un valor alto (cercano a 1)** porque el patrón de preferencia es idéntico. Sin embargo, la **Distancia Euclidiana se disparará**, penalizando al sistema al interpretar falsamente que sus gustos son totalmente opuestos.
    
    2. **Normalización intrínseca:** La similitud coseno cuenta con una normalización por las normas $(\|\mathbf{{u}}\|\|\mathbf{{v}}\|)$ incorporada en su denominador. Esto remueve el sesgo de los usuarios que califican de manera muy generosa o muy estricta, cualidad de la que carece la distancia euclidiana clásica.
    
    3. **Vedicto de Ingeniería:** Para este proyecto de asignación de películas, la **Similitud Coseno es técnicamente superior**. En bases de datos reales masivas (como el dataset de la Fase II), los usuarios rara vez ven las mismas películas, provocando que los vectores sean altamente dispersos (*sparse vectors*). El coseno gestiona de manera óptima las direcciones en espacios de alta dimensionalidad sin verse afectado por la cantidad total de películas puntuadas.
    """)

    # =====================================================
    # SIMULADOR INTERACTIVO DE ÁNGULO 
    # =====================================================
    st.write("---")
    st.subheader("Simulador Interactivo: Del Ángulo Geométrico a la Similitud")

    st.write("""
    Para interiorizar la intuición geométrica detrás de esta métrica, experimenta con el siguiente control. 
    Mueve el deslizador para cambiar el ángulo ($\theta$) entre dos vectores teóricos y observa cómo impacta en el valor del coseno y en su interpretación.
    """)

    # Slider interactivo de 0 a 180 grados
    angulo_slider = st.slider(
        label="Selecciona el ángulo (θ) en grados:",
        min_value=0,
        max_value=180,
        value=45,  # Valor inicial por defecto
        step=1,
        format="%d°"
    )

    # Convertir a radianes para las funciones trigonométricas de numpy
    radianes = np.radians(angulo_slider)
    coseno_calculado = np.cos(radianes)

    # Mostrar el resultado de manera llamativa
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        st.metric(
            label="Ángulo Seleccionado", 
            value=f"{angulo_slider}°", 
            help="Ángulo de apertura geométrica entre los dos vectores."
        )
    with sim_col2:
        st.metric(
            label="Valor del Coseno (Similitud)", 
            value=f"{coseno_calculado:.4f}",
            help="Resultado de aplicar la función coseno. Equivale al índice de similitud."
        )

    # Gráfico interactivo simple para ilustrar la apertura del ángulo
    fig_sim, ax_sim = plt.subplots(figsize=(4, 4))
    # Vector base fijo (en el eje X)
    ax_sim.quiver(0, 0, 1, 0, angles='xy', scale_units='xy', scale=1, color='#1E88E5', label="Vector U (Fijo)")
    # Vector móvil según el slider
    ax_sim.quiver(0, 0, np.cos(radianes), np.sin(radianes), angles='xy', scale_units='xy', scale=1, color='#D81B60', label="Vector V (Móvil)")
    
    ax_sim.set_xlim(-1.2, 1.2)
    ax_sim.set_ylim(-1.2, 1.2)
    ax_sim.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax_sim.axvline(0, color='gray', linestyle='--', alpha=0.5)
    ax_sim.set_title(f"Apertura Angular: {angulo_slider}°")
    ax_sim.grid(True, linestyle=':', alpha=0.6)
    ax_sim.legend(loc="lower left")
    
    # Renderizar el gráfico pequeño al lado o centrado
    st.pyplot(fig_sim)

    # Explicación del significado físico/analítico en tiempo real
    st.write("#### 📢 Significado en el Sistema de Recomendación:")

    if angulo_slider == 0:
        st.success(
            f"🎯 **Ángulo de {angulo_slider}° (Coseno = {coseno_calculado:.1f}): Coincidencia Absoluta.** "
            "Los vectores son colineales y apuntan exactamente en la misma dirección. En un entorno real, significa que "
            "ambos perfiles tienen proporciones de gustos idénticas. Las recomendaciones tendrán un 100% de confianza."
        )
    elif angulo_slider < 45:
        st.success(
            f"🟢 **Ángulo de {angulo_slider}° (Coseno = {coseno_calculado:.4f}): Alta Similitud.** "
            "El ángulo es cerrado. Los usuarios tienden fuertemente a disfrutar y rechazar los mismos contenidos. "
            "Es el escenario ideal para el filtrado colaborativo."
        )
    elif angulo_slider < 90:
        st.info(
            f"🟡 **Ángulo de {angulo_slider}° (Coseno = {coseno_calculado:.4f}): Similitud Moderada a Baja.** "
            "Los vectores empiezan a abrirse. Hay algunos puntos de encuentro, pero las diferencias en las preferencias "
            "comienzan a ser notorias."
        )
    elif angulo_slider == 90:
        st.warning(
            f"⚪ **Ángulo de {angulo_slider}° (Coseno = {coseno_calculado:.1f}): Ortogonalidad (Sin relación).** "
            "Los vectores son perpendiculares. Matemáticamente, el producto punto es 0. Significa que los gustos "
            "de los usuarios son completamente independientes; lo que a uno le apasiona, al otro le resulta indiferente. "
            "No se pueden generar recomendaciones basadas en este par."
        )
    elif angulo_slider < 135:
        st.error(
            f"🟠 **Ángulo de {angulo_slider}° (Coseno = {coseno_calculado:.4f}): Preferencias Inversas.** "
            "El ángulo es obtuso. Los usuarios muestran una tendencia opuesta. Nota: Esto ocurre habitualmente si los "
            "datos han sido normalizados restando la calificación promedio de la plataforma (valores negativos y positivos)."
        )
    else:
        st.error(
            f"🔴 **Ángulo de {angulo_slider}° (Coseno = {coseno_calculado:.4f}): Oposición Total.** "
            "Los vectores apuntan en direcciones contrarias. Lo que a un usuario le encanta (calificación máxima), al otro "
            "le desagrada por completo (calificación mínima). En ingeniería de software, este dato se podría usar para "
            "un 'sistema de recomendación inverso' (recomendar lo que sabemos que NO le gustará)."
        )