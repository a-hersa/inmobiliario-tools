# Imagen base de Python
FROM python:3.12

# Establecer el directorio de trabajo
RUN mkdir /code
WORKDIR /code

# Instalar dependencias de Python
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copiar el código de la aplicación
COPY . /code/

# Comando para iniciar la aplicación
CMD ["shiny", "run", "--host=0.0.0.0", "--port=8000", "app.py"]
