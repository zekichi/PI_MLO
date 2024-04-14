import pandas as pd



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

def UsersRecommend(año: int):
    df = pd.read_csv('datasets/recommend.csv')
    
    # Filtrar el DataFrame por el año especificado
    result_df = df[df['año'] == año]

    response_data = [{"Puesto 1": result_df.iloc[0]['name']},
                     {"Puesto 2": result_df.iloc[1]['name']},
                     {"Puesto 3": result_df.iloc[2]['name']}]

    return response_data
