import scrapy
from datetime import datetime
from ..items import PropertyItem
from ..utils import extract_location_from_title


class PropiedadesSpider(scrapy.Spider):
    name = "propiedades"
    allowed_domains = ["idealista.com", "api.scrapingant.com"]

    # Puedes agregar más URLs a esta lista
    start_urls = [
        'https://www.idealista.com/venta-viviendas/premia-de-mar-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,ultimas-plantas,plantas-intermedias/',
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
            # Extrae los datos directamente del listado
            propiedad = PropertyItem()
            
            # URL del enlace de la propiedad
            relative_url = container.css('a.item-link::attr(href)').get()
            if relative_url:
                full_url = response.urljoin(relative_url)
                # Extract p_id as integer from URL (e.g., from /inmueble/107435644/ get 107435644)
                try:
                    p_id_str = full_url.rstrip('/').split('/')[-1]
                    propiedad['p_id'] = int(p_id_str)
                except (ValueError, IndexError):
                    # Fallback: skip this property if p_id extraction fails
                    continue
                propiedad['url'] = full_url
            
            # Nombre/título de la propiedad
            raw_title = container.css('a.item-link::text').get()
            
            # Extract location from title and clean title
            if raw_title:
                clean_title, location = self.extract_location_from_title(raw_title)
                propiedad['nombre'] = clean_title
                propiedad['poblacion'] = location
            else:
                propiedad['nombre'] = ""
                propiedad['poblacion'] = ""
            
            # Precio
            propiedad['precio'] = container.css('span.item-price::text').get()
            
            # Información adicional (metros, habitaciones, etc.)
            detail_items = container.css('span.item-detail::text').getall()
            propiedad['metros'] = ""
            propiedad['habitaciones'] = ""
            propiedad['planta'] = ""
            propiedad['ascensor'] = 0  # Default to 0
            
            if detail_items:
                # Buscar metros cuadrados y ascensor
                for detail in detail_items:
                    if 'm²' in detail:
                        propiedad['metros'] = detail.replace('m²', '').strip()
                    elif 'hab.' in detail:
                        propiedad['habitaciones'] = detail.replace('hab.', '').strip()
                    elif 'planta' in detail.lower():
                        propiedad['planta'] = detail.strip()
                    elif 'con ascensor' in detail.lower():
                        propiedad['ascensor'] = 1
            
            # Descripción (si está disponible en el listado)
            propiedad['descripcion'] = container.css('p.item-description::text').get()
            
            # Campos adicionales con valores por defecto
            propiedad['fecha_crawl'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            propiedad['estatus'] = "activo"
            
            yield propiedad

        # Opcional: Si la página tiene paginación, puedes seguir los enlaces a las páginas siguientes
        next_page = response.css('a.icon-arrow-right-after::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
