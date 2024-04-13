from fastapi import FastAPI, HTTPException
from functions import *
import pandas as pd

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