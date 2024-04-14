from fastapi import FastAPI, HTTPException
from functions import *
import pandas as pd
import traceback
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root():
    return "Hola mundo"

# Endpoint 1

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