FROM python:3.11.7-slim-bullseye
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

#CMD python app.py
CMD gunicorn --bind 0.0.0.0:5000 -w 3 app:app