import pandas as pd


#---- primer endpoint ----

def PlayTimeGenre(genero: str):
    df = pd.read_csv('datasets/año_genres.csv')

    # Filtrar el DataFrame para el género específico
    filtered_df = df[df['genres'] == genero]
    
    # Agrupar por año de lanzamiento y sumar las horas jugadas
    grouped_df = filtered_df.groupby('año')['horas'].sum()
    
    # Encontrar el año con más horas jugadas
    año_max = grouped_df.idxmax()

    # Construye el response_data
    response = {"Año de lanzamiento con más horas jugadas para {}: {}".format(genero, año_max)}

    # Muestra el resultado
    return response


#---- segundo endpoint ----

def UserForGenre(genre: str):
    # Leer el archivo CSV
    user_genre_data = pd.read_csv('datasets/genre_user.csv')
    
    # Filtrar el DataFrame por el género dado
    genre_data = user_genre_data[user_genre_data['genres'] == genre]

    # Encontrar al usuario con más horas jugadas para ese género
    top_user = genre_data.loc[genre_data['horas'].idxmax(), 'user_id']

    # Calcular la suma de horas jugadas por año
    horas_por_año = genre_data.groupby('año')['horas'].sum().reset_index()
    
    # Convertir el DataFrame a una lista de diccionarios
    hours_list = horas_por_año.to_dict(orient='records')

    # Crear el diccionario de retorno
    result = {
        f"Usuario con más horas jugadas para Género {genre}": top_user,
        "Horas jugadas": hours_list
    }

    return result


#---- tercer endpoint ----


def UsersRecommend(año: int):
    df = pd.read_csv('datasets/recomennd.csv')
    
    # Filtrar el DataFrame por el año especificado
    result_df = df[df['año'] == año]

    response_data = [{"Puesto 1": result_df.iloc[0]['name']},
                     {"Puesto 2": result_df.iloc[1]['name']},
                     {"Puesto 3": result_df.iloc[2]['name']}]

    return response_data


#---- cuarto endpoint ----

def UsersWorstDeveloper(año: int):
    df = pd.read_csv('worst_developer.csv')

    # Filtrar el DataFrame por el año especificado
    result_df = df[df['año'] == año]

    if result_df.empty:
        return "No hay datos disponibles para el año especificado."

    # Ordenar por rendimiento y seleccionar los tres peores
    result_df = result_df.nsmallest(3, 'performance')

    # Construir la respuesta
    response_data = [{"Puesto {}: ".format(i+1): developer} for i, developer in enumerate(result_df['developer'])]

    return response_data


#---- quinto endpoint ----

def sentiment_analysis(empresa_desarrolladora: str):
    df = pd.read_csv('sentiment_analysis.csv')

    # Filtrar por la empresa desarrolladora
    result_df = df[df['developer'] == empresa_desarrolladora]

    if result_df.empty:
        return {"message": f"No hay datos disponibles para la empresa desarrolladora '{empresa_desarrolladora}'."}

    # Seleccionar columnas relevantes y convertir a diccionario
    response_data = result_df[['Negative', 'Neutral', 'Positive']].to_dict(orient='records')[0]
    
    return {empresa_desarrolladora: response_data}


#---- modelo endpoint ----

def recomendacion_usuario(item_id):
    df = pd.read_csv('model_recommend.csv')
    
    # Filtrar el DataFrame por el item_id especificado
    result_df = df[df['item_id'] == item_id]
    
    if result_df.empty:
        return {"message": f"No se encontraron recomendaciones para el item con ID {item_id}."}
    
    # Obtener las recomendaciones como una lista de strings
    recomendaciones = result_df['Recomendaciones'].tolist()
 
    return {"recomendaciones": recomendaciones}