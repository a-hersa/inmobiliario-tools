import scrapy
from ..items import PropertyItem


class NovedadesSpider(scrapy.Spider):
    name = "novedades"
    allowed_domains = ["idealista.com", "api.scrapingant.com"]
    
    # Puedes agregar más URLs a esta lista
    start_urls = [
        'https://www.idealista.com/venta-viviendas/premia-de-mar-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/argentona-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/sant-pol-de-mar-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/canet-de-mar-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/caldes-d-estrac-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/arenys-de-mar-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/mataro-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/',
        'https://www.idealista.com/venta-viviendas/granollers-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/'
    ]


    def parse(self, response):
        # Selecciona todos los divs con la clase 'item-info-container'
        containers = response.css('div.item-info-container')
        print(f'number of properties in this page is {len(containers)}')

        for container in containers:
            # Extrae el href del primer enlace dentro del contenedor
            relative_url = container.css('a.item-link::attr(href)').get()
            
            if relative_url:
                # Construye la URL completa
                full_url = response.urljoin(relative_url)
                
                # Aquí podrías seguir a la URL o simplemente imprimirla
                yield scrapy.Request(full_url, callback=self.parse_item)

        # Opcional: Si la página tiene paginación, puedes seguir los enlaces a las páginas siguientes
        next_page = response.css('a.icon-arrow-right-after::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        propiedad = PropertyItem()
        propiedad['p_id'] = response.url
        propiedad["nombre"] = response.css('span.main-info__title-main::text').get()
        propiedad["fecha_idealista"] = response.css('#stats > p::text').get()
        propiedad["precio"] = response.css('span.info-data-price > span.txt-bold::text').get()
        propiedad["metros"] = response.css('div.info-features > span::text').getall()[0] 
        propiedad["habitaciones"]= response.css('div.info-features > span::text').getall()[1]
        propiedad["planta"] = response.css('div.info-features > span::text').getall()[2]
        propiedad["ascensor"] = response.css('div.info-features > span::text').getall()[2]
        propiedad["poblacion"] = response.css('span.main-info__title-minor::text').get()
        propiedad["url"] = response.url
        propiedad["descripcion"] = response.css('div.adCommentsLanguage > p::text').get()
        yield propiedad
