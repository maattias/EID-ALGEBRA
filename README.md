# Sistema de Recomendación de Películas con Álgebra Lineal

Proyecto de Investigación 6 - Álgebra Lineal para la Computación

## Descripción

Este proyecto implementa una aplicación web en Python para recomendar películas usando filtrado colaborativo basado en similitud coseno.

A partir del dataset MovieLens 100K, la aplicación construye una matriz usuario-película, compara usuarios según sus valoraciones y genera recomendaciones personalizadas para un usuario objetivo.

El enfoque principal del proyecto es aplicar conceptos de álgebra lineal, especialmente representación matricial, vectores, producto punto, norma euclidiana y similitud coseno.

## Fundamento matemático

Cada usuario se representa como un vector de valoraciones:

    Usuario u = [rating_1, rating_2, rating_3, ..., rating_n]


Cada posición del vector representa la valoración que el usuario dio a una película. Si el usuario no valoró una película, ese dato se trata como faltante para la recomendación y como cero para el cálculo vectorial de similitud.

La similitud entre dos usuarios se calcula mediante similitud coseno:

    cos(theta) = (u · v) / (||u|| · ||v||)

Donde:

    u · v   = producto punto entre los vectores
    ||u||   = norma euclidiana del vector u
    ||v||   = norma euclidiana del vector v

Mientras más cercano sea el resultado a 1, mayor será la similitud entre ambos usuarios.

## Funcionalidades

* Carga del dataset MovieLens 100K.
* Construcción de la matriz usuario-película.
* Cálculo de similitud coseno entre usuarios.
* Visualización de matriz de similitud mediante mapa de calor.
* Generación de recomendaciones personalizadas.
* Análisis exploratorio del dataset.
* Explicación interactiva de la matemática utilizada.
* Pruebas unitarias para validar los cálculos principales.

## Dataset

Se utiliza el dataset MovieLens 100K, compuesto por archivos de valoraciones, películas y usuarios.

La carpeta debe tener esta estructura:

    data/
    └── ml-100k/
        ├── u.data
        ├── u.item
        └── u.user


Archivos utilizados:

    u.data   -> valoraciones de usuarios a películas
    u.item   -> información de películas
    u.user   -> información de usuarios


## Instalación

Instalar las dependencias:

    pip install -r requirements.txt


## Ejecución

Ejecutar la aplicación con Streamlit:

    streamlit run app.py


La aplicación quedará disponible en:

    http://localhost:8501


## Pruebas

Ejecutar las pruebas unitarias con:

    pytest tests/test_similarity.py


Estas pruebas validan:

producto punto
norma euclidiana
similitud coseno entre dos vectores
matriz de similitud entre usuarios
casos ortogonales
manejo de vectores sin valoraciones


## Estructura del proyecto

sistema-recomendacion/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── INSTRUCCIONES_DATASET.md
│   └── ml-100k/
│       ├── README
│       ├── u.data
│       ├── u.item
│       └── u.user
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── recommender.py
│   └── model/
│       └── similarity.py
│
├── ui/
│   ├── __init__.py
│   ├── sidebar.py
│   ├── styles.py
│   └── tabs/
│       ├── tab_analisis.py
│       ├── tab_matematicas.py
│       ├── tab_recomendaciones.py
│       └── tab_similitud.py
│
└── tests/
    ├── pruebas.ipynb
    └── test_similarity.py
```

## Descripción de archivos

### app.py

Archivo principal de la aplicación. Configura Streamlit, inicializa los datos, llama a las funciones de carga y procesamiento, guarda la matriz usuario-película y la matriz de similitud en memoria, y renderiza las pestañas principales.

### src/data_loader.py

Contiene funciones para cargar y limpiar los archivos del dataset MovieLens 100K. También define la función encargada de construir la matriz usuario-película y calcular estadísticas básicas del dataset.

Funciones principales:

    cargar_dataset()
    construir_matriz_usuario_pelicula()
    obtener_lista_usuarios()
    obtener_peliculas_usuario()
    obtener_estadisticas()


### src/model/similarity.py

Contiene la lógica matemática principal del proyecto.

Funciones principales:

    calcular_producto_punto()
    calcular_norma()
    calcular_similitud_coseno()
    obtener_pasos_similitud_coseno()
    calcular_matriz_similitud()


### src/recommender.py

Contiene la lógica de recomendación. Usa la matriz de similitud para buscar usuarios vecinos y calcular puntajes predichos para películas que el usuario objetivo no ha valorado.

Funciones principales:

    obtener_k_vecinos()
    predecir_puntajes()
    recomendar()
    recomendar_con_titulos()


### ui/sidebar.py

Contiene los controles laterales de la aplicación:

    selector de usuario objetivo
    número de vecinos similares
    número de recomendaciones
    tamaño de muestra para el heatmap
    resumen del dataset


### ui/styles.py

Contiene estilos CSS básicos para mejorar la visualización de la app en Streamlit.

### ui/tabs/tab_analisis.py

Muestra estadísticas generales del dataset:

    cantidad de usuarios
    cantidad de películas
    cantidad de valoraciones
    densidad de la matriz
    distribución de ratings
    películas más valoradas
    películas con mejor promedio


### ui/tabs/tab_matematicas.py

Explica los fundamentos matemáticos mediante una matriz pequeña de ejemplo. Muestra paso a paso el producto punto, las normas vectoriales y la similitud coseno.

### ui/tabs/tab_similitud.py

Visualiza la similitud real entre usuarios usando el dataset MovieLens. Incluye mapa de calor, usuarios más similares y comparación entre el usuario objetivo y su vecino más cercano.

### ui/tabs/tab_recomendaciones.py

Genera recomendaciones personalizadas para el usuario seleccionado en el sidebar. Muestra usuarios similares, películas recomendadas y el historial de valoraciones del usuario.

### tests/test_similarity.py

Contiene pruebas unitarias para validar que los cálculos matemáticos funcionen correctamente.

## Tecnologías utilizadas

* Python
* Streamlit
* NumPy
* Pandas
* Matplotlib
* Pytest

