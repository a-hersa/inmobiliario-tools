FROM python:3.11.7-slim-bullseye
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD [ "scrapy", "crawl", "novedades" ]