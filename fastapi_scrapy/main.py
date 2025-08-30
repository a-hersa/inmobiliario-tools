from fastapi import FastAPI
from pydantic import BaseModel
import asyncpg
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from inmobiliario.spiders.propiedades import PropiedadesSpider

DB_USER = os.getenv("POSTGRES_USER", "mi_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "mi_pass")
DB_NAME = os.getenv("POSTGRES_DB", "inmobiliario_db")
DB_HOST = "postgres"

app = FastAPI()


class MunicipioRequest(BaseModel):
    nombre: str
    url: str


class ActivateRequest(BaseModel):
    municipio_id: int
    spider_name: str = "propiedades"


async def get_connection():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
        port=5432
    )


@app.post("/add_municipio/")
async def add_municipio(req: MunicipioRequest):
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """INSERT INTO municipios (nombre, url)
               VALUES ($1, $2)
               ON CONFLICT (url) DO UPDATE SET nombre=EXCLUDED.nombre
               RETURNING id, nombre, url""",
            req.nombre, req.url
        )
    finally:
        await conn.close()
    return dict(row)


@app.post("/activate_municipio/")
async def activate_municipio(req: ActivateRequest):
    conn = await get_connection()
    try:
        await conn.execute(
            """INSERT INTO start_urls (municipio_id, spider_name)
               VALUES ($1, $2)
               ON CONFLICT (municipio_id, spider_name) DO NOTHING""",
            req.municipio_id, req.spider_name
        )
    finally:
        await conn.close()
    return {"status": "activated", "municipio_id": req.municipio_id}


@app.post("/run_spider/")
async def run_spider(spider_name: str = "propiedades"):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(PropiedadesSpider)
    process.start()
    return {"status": "spider finished", "spider": spider_name}
