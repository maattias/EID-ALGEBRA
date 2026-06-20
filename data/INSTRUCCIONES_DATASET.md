# Instrucciones para usar el dataset MovieLens 100K

## 1. Dataset seleccionado

El proyecto utiliza **MovieLens 100K**, un dataset público de valoraciones de películas creado por GroupLens.

Fuente oficial:

https://grouplens.org/datasets/movielens/100k/

Este dataset contiene valoraciones de usuarios sobre películas y es adecuado para construir una matriz usuario-producto y aplicar similitud coseno.

## 2. Descarga

1. Entrar a la página oficial:
   https://grouplens.org/datasets/movielens/100k/

2. Descargar el archivo:

   `ml-100k.zip`

3. Descomprimir el archivo.

4. Copiar la carpeta descomprimida dentro de `data/`.

La estructura final debe quedar así:

```txt
proyecto/
└── data/
    ├── INSTRUCCIONES_DATASET.md
    └── ml-100k/
        ├── u.data
        ├── u.item
        ├── u.user
        └── README