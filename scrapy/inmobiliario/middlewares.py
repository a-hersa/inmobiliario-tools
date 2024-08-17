import http.client
from urllib.parse import quote
from scrapy import signals
import scrapy
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class ScrapingAntProxyMiddleware:
    def __init__(self):
        self.api_key = f'{os.getenv("SCRAPINGANT")}'  # Reemplaza con tu clave API
        self.base_url = "api.scrapingant.com"
        self.browser = "&browser=false"
        self.proxy_country = "" # "&proxy_country=ES"

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Codifica la URL original
        encoded_url = quote(request.url, safe='')

        # Crea la conexión HTTPS con ScrapingAnt
        conn = http.client.HTTPSConnection(self.base_url)

        # Construye la nueva URL con el proxy y otros parámetros
        api_request_path = f"/v2/general?url={encoded_url}&x-api-key={self.api_key}{self.browser}{self.proxy_country}"

        # Realiza la solicitud al proxy
        conn.request("GET", api_request_path)
        res = conn.getresponse()
        
        # Si la respuesta es exitosa, reemplazamos el cuerpo de la respuesta en Scrapy
        if res.status == 200:
            response_data = res.read()
            # Crea una nueva respuesta con los datos obtenidos del proxy
            new_response = scrapy.http.HtmlResponse(
                url=request.url,
                body=response_data,
                encoding='utf-8',
                request=request
            )
            return new_response
        else:
            spider.logger.error(f"Failed to process proxy request: {res.status} {res.reason}")
            return None

    def process_exception(self, request, exception, spider):
        # Manejo de excepciones para reintentar la solicitud en caso de error
        spider.logger.error(f"Exception occurred: {exception}")
        return request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
