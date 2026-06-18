# Sistema de Recomendación de Películas con Álgebra Lineal

Proyecto de Investigación 6 – MATE1187 Álgebra Lineal para la Computación

## Descripción

Este proyecto consiste en una aplicación web desarrollada en Python que implementa un sistema de recomendación de películas utilizando filtrado colaborativo basado en similitud coseno.

A partir de las valoraciones registradas en el dataset MovieLens 100K, el sistema identifica usuarios con preferencias similares y genera recomendaciones personalizadas de películas.

El objetivo es aplicar conceptos de álgebra lineal vistos en la asignatura, especialmente el uso de vectores, productos punto y medidas de similitud.

### Instalar dependencias

pip install -r requirements.txt

### Descargar el dataset

Seguir las instrucciones indicadas en:

data/INSTRUCCIONES_DATASET.md

### Ejecutar la aplicación

streamlit run app.py

La aplicación estará disponible en:

http://localhost:8501

## Estructura del proyecto

sistema-recomendacion/
│
├── app.py
├── requirements.txt
├── README.md
├── PLAN_DE_TRABAJO.md
│
├── src/
│   ├── data_loader.py
│   ├── similarity.py
│   └── recommender.py
│
├── ui/
│   ├── styles.py
│   ├── sidebar.py
│   ├── components.py
│   └── tabs/
│       ├── tab_recomendaciones.py
│       ├── tab_analisis.py
│       ├── tab_similitud.py
│       └── tab_matematicas.py
│
└── data/
    └── INSTRUCCIONES_DATASET.md

## Fundamento matemático

Cada usuario se representa mediante un vector que contiene las valoraciones realizadas a distintas películas. Para medir la semejanza entre dos usuarios se utiliza la similitud coseno

Mientras más cercano sea el resultado a 1, mayor será la similitud entre ambos perfiles de usuario.

## Funcionalidades

* Generación de recomendaciones personalizadas.
* Comparación de usuarios mediante similitud coseno.
* Visualización de estadísticas del dataset.
* Análisis de valoraciones y patrones de recomendación.
* Explicación interactiva de los conceptos matemáticos utilizados.

## Dataset

Se utiliza el conjunto de datos **MovieLens 100K**, desarrollado por GroupLens Research de la Universidad de Minnesota.

## Referencia:

Harper, F. M., & Konstan, J. A. (2015). *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems, 5(4), 1–19.

## Tecnologías utilizadas

* Python 3.11
* Streamlit
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Plotly
