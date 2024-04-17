from fastapi import FastAPI, HTTPException
from functions import *
import pandas as pd
import traceback
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root():
    return "Hola mundo"

# ------- Endpoint 1 -------

@app.get("/PlayTimeGenre/{genero}", tags=['PlayTimeGenre'])
async def endpoint1(genero: str):
    """
    Descripción: Retorna el año con más horas jugadas para un género dado.
    
    Parámetros:
        - genero (str): Género para el cual se busca el año con más horas jugadas. Debe ser un string, ejemplo: Action
    
    Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género Action" : 2012}
    """
    try:
        # Validación adicional para asegurarse de que el género no sea nulo o esté vacío
        if not genero or not genero.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'genero' no puede ser nulo o estar vacío.")

        result = PlayTimeGenre(genero)
    
        # Validación para verificar si el género existe en los datos
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontró información para el género '{genero}'.")

        return result
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo año_genre.csv: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    


# ------- Endpoint 2 -------

@app.get("/UserForGenre/{genero}", tags=['UserForGenre'])
async def endpoint2(genero: str):
    try:
        # Validar el parámetro de género
        if not genero or not genero.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'genero' no puede ser nulo o estar vacío.")

        # Obtener los datos para el género dado
        genre_data = UserForGenre(genero)
        
        # Validar si se encontraron datos para el género
        if not genre_data:
            raise HTTPException(status_code=404, detail=f"No se encontró información para el género '{genero}'.")

        return genre_data
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo UserForGenre.csv: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

# ------- Endpoint 3 -------

@app.get("/UsersRecommend/{año}", tags=['UsersRecommend'])
async def endpoint3(año: str):
    try:
        año = int(año)
    
        if not (2000 <= año <= 2100):
            error_message = f"El año debe estar en el rango entre 2000 y 2100."
            return JSONResponse(status_code=400, content={"error": error_message})
        
        result = UsersRecommend(año)
        return result

    except ValueError:
        error_message = "El año debe ser un número entero."
        return JSONResponse(status_code=400, content={"error": error_message})


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def server_error_exception_handler(request, exc):
    error_message = "Error interno del servidor."
    return JSONResponse(status_code=500, content={"error": error_message})


# ------- Endpoint 4 -------

@app.get("/UsersWorstDeveloper/{year}", tags=['UsersWorstDeveloper'])
async def endpoint4(año: str):
    """
    Descripción: Retorna el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
    
    Parámetros:
        - year (str): Año para el cual se busca el top 3 de desarrolladoras menos recomendadas. Debe ser número de 4 dígitos, ejemplo: 2015

    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    """
    try:
        year = int(año)
        if not (1000 <= año <= 9999):
            raise ValueError("El año debe ser un número de 4 dígitos.")
        result = UsersWorstDeveloper(año)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo UsersWorstDeveloper.csv: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

# ------- Endpoint 5 -------

@app.get("/sentiment_analysis/{empresa_desarrolladora}", tags=['sentiment_analysis'])
async def enpoint5(empresa_desarrolladora: str):
    """
    Descripción: Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    
    Parámetros:
        - empresa_desarrolladora (str): Nombre de la empresa desarrolladora para la cual se realiza el análisis de sentimiento. Debe ser un string, ejemplo: Valve
    
    Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}
    """
    try:
        # Validar que el nombre de la empresa no esté vacío
        if not empresa_desarrolladora:
            raise ValueError("El nombre de la empresa desarrolladora no puede estar vacío.")
        
        result = sentiment_analysis(empresa_desarrolladora)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo sentiment_analysis.csv: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

# ------- Endpoint ML -------

@app.get("/item/{item_id}", tags=['item'])
async def item(item_id: int):
    """
    Descripción: Ingresando el id de producto, devuelve una lista con 5 juegos recomendados similares al ingresado.
    
    Parámetros:
        - item_id (str): Id del producto para el cual se busca la recomendación. Debe ser un número, ejemplo: 761140
        
    Ejemplo de retorno: "['弹炸人2222', 'Uncanny Islands', 'Beach Rules', 'Planetarium 2 - Zen Odyssey', 'The Warrior Of Treasures']"

    """
    try:
        # Validar que el item_id sea un entero
        if not isinstance(item_id, int):
            raise ValueError("El item_id debe ser un número entero.")
        
        resultado = recomendacion_usuario(item_id)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo de recomendaciones: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
