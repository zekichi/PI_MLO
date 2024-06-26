# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="scr/caratula.png"  height=300>
</p>


- ## **`Links`**
    - [API desplegada en Render](https://pi-mlo.onrender.com/docs)
    - [Link al video](https://www.loom.com/share/64928241529240eabb615c9d19ccb764?sid=ba2344a2-94d9-4864-a6ee-e9a06a57b53e)

<hr>

# descripción

## **Descripción del problema (Contexto y rol a desarrollar)**

Desarrollaremos un modelos de recomendación lo cual nos parece muy bueno y con un muy buen rendimiento, por lo cual lo pondermos a prueba con unos datasets de steam. Vamos a tomar un rol de Data Science de Steam (plataforma multinacional de videjuegos), empresa para la cual desarrolaremos un sistema de recomendación de videojuegos para usuarios.

En nuestro trabajos con los datos pudimos ver que la madurez de los mismos es practicamente nula, por lo que empezaremos desde 0 para lograr obtener un buen MVP.


## **Propuesta de trabajo (requerimientos de aprobación)**

Para este objetivo del MVP no necesitaremos de hacer alguna transformación de datos. Por ende nos centraremos en leer el dataset con el formato correcto. Eliminaremos columnas que no sean relevantes para nuestro trabajo en nuestro armado de la API y el entrenamiento de nuestro modelo.

En el dataset user_reviews encontraremos reseñas de users, con las cuales procederemos a crear una columna la cual llamaremos 'sentiment_analysis' aplicando un análisi de sentimiento con el siguiente criterio:
- '0' si es una reseña mala.
- '1' si es una reseña neutral.
- '2' si es una reseña positiva.  
Esta columna reemplazara la de users_reviews.review , asi facilitaremos el trabajo de los modelos de maching learning y el análisis de datos. De no existin tal reseña a analizar, toma el valor de '1', como si fuera una reseña neutral.

## **Desarrollo de la API**

Por medio del framework FastAPI trabajaremos con nuestros endpoints que serán los siguientes.

**`Endpoints`**: decorado(@app.get('/')).
- def PlayTimeGenre(genero : str): Este devolverá el año con mayor horas de juego para el genero dado.
- def UserForGenre(genero : str): Este devolverá el usuario que posee el mayor timepo de juego para un genero dado(en formato de horas), y además una lista de la cantidad de horas por cada año.
- def UserRecommend(año : int): Este devolverá los 3 primeros juegos con mayor recomendaciones por usuario para el año dado. reviews.recommend = True y comentarios positivos/neutrales.
- def UsersWorstDeveloper(año : int): Este devolverá los 3 primeros desarrolladoras con juegos menos recomendados para el año dado. review.recommend = False y comentarios negativos.
-def sentiment_analysis(desarrollador : str): Este devolverá un diccionario con el nombre de la empresa como llave y una lista con la cantidad de registros de reseñas que est´qn categorizadas con un análisi de sentimiento.

La API será consumida según criterios de APIRest o RESTful, por cualquier dispositivop conectado a internet.

**`Deployment`**: El deploy será a travez de Render.

## **EDA**

Ahora que ya poseemos unos datasets con los datos limpios, nos toca analizar las relaciones entre las variables en busca de si existen outliers o alguna anomalía. Estaremos bien atentos a la prescencia de algún buen patrón con el cuál realizar un análisis posterior. Para una mejor practica y aplicación de conocimientos aprendidos esta vez no haremos uso de librerías para EDA automático.

## **Modelo**

Ya teninendo una data completamente consumible por la API, procederemos a entrenar nuesto modelo de machine learning para el armado de un sistema de recomendación.

Nuestro modelo de recomendación tendrá una relación de item-item, lo que toma un item y recomienda otro parecido. El valor de entrada sera un juego y el valor de salida será una lista de 5 juegos recomendados, para el cual usaremos la similitud del coseno.

-def recomendación_juego(item_id): Esto devolverá una lista con 5 juegos recomendados similares al ingresado.
