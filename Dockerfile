# Usar una imagen base de Python
FROM python:3.8-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación y los requerimientos
COPY requirements.txt .
COPY main.py .
COPY funciones.py .
COPY model/* ./model/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos de datos desde el repositorio de GitHub
COPY datasets/* ./datasets/

# Expone el puerto en el que la aplicación FastAPI se ejecutará
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI cuando se inicie el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]