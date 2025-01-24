# Imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /code

# Copiar el archivo de dependencias
COPY requirements.txt requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando para iniciar la aplicación
CMD ["shiny", "run", "--host=0.0.0.0", "--port=8000", "app.py"]
