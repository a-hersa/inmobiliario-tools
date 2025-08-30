FROM python:3.11.7-slim-bullseye
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && \
    apt-get install -y gcc libxml2-dev libxslt1-dev && \
    pip install --no-cache-dir -r requirements.txt
COPY . /code/

# Exponer puerto de FastAPI
EXPOSE 8000

# Comando de arranque FastAPI
CMD ["uvicorn", "fastapi_scrapy.main:app", "--host", "0.0.0.0", "--port", "8000"]
