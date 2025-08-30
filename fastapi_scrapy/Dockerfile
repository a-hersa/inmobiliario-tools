FROM python:3.11.7-slim-bullseye

# Crear directorio de trabajo
RUN mkdir /code
WORKDIR /code

# Copiar y instalar dependencias
COPY fastapi_scrapy/requirements.txt /code/
RUN apt-get update && \
    apt-get install -y gcc libxml2-dev libxslt1-dev libpq-dev && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de fastapi_scrapy al contenedor
COPY fastapi_scrapy/ /code/

# Exponer puerto de FastAPI
EXPOSE 8000

# Comando de arranque FastAPI
# Usamos 'main:app' porque 'main.py' está directamente en /code/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
