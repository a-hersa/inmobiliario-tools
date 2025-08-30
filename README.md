## .env file
Edit the env-template file

## Commands
`docker-compose ps`

`docker-compose up`

`docker-compose down`

`docker-compose build`

`docker-compose up --build -d`

### UFW
add ports in server's dashboard


## Cronjob
0 7 * * * cd [WORKDIR] && sudo docker exec inmobiliario-scrapy scrapy crawl propiedades

```
curl -X POST "http://localhost:8000/add_municipio/" \
-H "Content-Type: application/json" \
-d '{"nombre":"Mataró","url":"https://www.idealista.com/venta-viviendas/mataro-barcelona/"}'
```

```
curl -X POST "http://localhost:8000/activate_municipio/" \
-H "Content-Type: application/json" \
-d '{"municipio_id": 1, "spider_name": "propiedades"}'
```


```
curl -X POST "http://localhost:8000/run_spider/"
```