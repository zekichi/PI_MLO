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