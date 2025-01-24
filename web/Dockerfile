FROM python:3.11.7-slim-bullseye

# Crear directorio de trabajo
RUN mkdir /code
WORKDIR /code

# Instalación de dependencias
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copia de archivos
COPY . /code/

# Comando para Flask en desarrollo
# CMD flask run --host=0.0.0.0 --port=5000

# Comando para Flask en producción
# CMD gunicorn --bind 0.0.0.0:5000 -w 3 app:app

# Comando variable según desarrollo o producción
CMD ["sh", "-c", "${FLASK_CMD}"]