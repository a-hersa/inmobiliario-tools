# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from inmobiliario.items import PropertyItem
import re
import psycopg2
from scrapy.exceptions import DropItem
from datetime import datetime
import os


class PropertyItemPipeline:
    def process_item(self, item, spider):
        # Verifica si el item es una instancia de PropertyItem
        if isinstance(item, PropertyItem):
            # Aquí puedes añadir las modificaciones que desees hacer al item.
            # Por ejemplo, puedes limpiar los datos, calcular nuevos valores, etc.

            # Ejemplo: Convertir el precio a un formato numérico
            item['p_id'] = self.convert_to_p_id(item['p_id'])

            item['fecha_idealista'] = self.convert_str_to_date(item['fecha_idealista'])

            item['precio'] = self.convert_price_to_number(item['precio'])

            item['metros'] = self.convert_meters_to_number(item['metros'])

            item['habitaciones'] = self.convert_rooms_to_number(item['habitaciones'])

            item['planta'] = self.convert_floor_to_number(item['planta'])

            item['ascensor'] = self.convert_lift_to_number(item['ascensor'])

            item['poblacion'] = self.extract_city(item['poblacion'])

            item['descripcion'] = self.smooth_text(item['descripcion'])

        return item  # Devuelve el item modificado
    
    def convert_to_p_id(self, url):
        try:
            p_id = url.split('/')[-2]
            return int(p_id)
        except:
            return 
        
    def convert_str_to_date(self, date_str):
        date_str = date_str.replace('Anuncio actualizado el ', '')
        year = datetime.now().year
        full_date_str = f"{date_str} {year}"

        month_translation = {
            "enero": "January",
            "febrero": "February",
            "marzo": "March",
            "abril": "April",
            "mayo": "May",
            "junio": "June",
            "julio": "July",
            "agosto": "August",
            "septiembre": "September",
            "octubre": "October",
            "noviembre": "November",
            "diciembre": "December"
        }

        for spanish_month, english_month in month_translation.items():
            if spanish_month in full_date_str.lower():
                full_date_str = full_date_str.lower().replace(spanish_month, english_month)
                break

        # Convertir el string a objeto datetime
        try:
            date_obj = datetime.strptime(full_date_str, "%d de %B %Y")
        except ValueError as e:
            print(f"Error converting date: {e}")

        # Convertir el objeto datetime a formato PostgreSQL
        postgres_date = date_obj.strftime("%Y-%m-%d")
        return postgres_date

    def convert_price_to_number(self, price_str):
        # Ejemplo: convertir una cadena de precio en un número
        # Elimina símbolos de moneda y comas, luego convierte a float
        price_str = price_str.replace('$', '').replace('.', '').strip()
        try:
            return int(price_str)
        except ValueError:
            return None
        
    def convert_meters_to_number(self, meters_str):
        meters_str = meters_str.replace('\n', '').replace(' m²', '')
        try:
            return int(meters_str)
        except ValueError:
            return None
        
    def convert_rooms_to_number(self, rooms_str):
        rooms_str = rooms_str.replace('\n', '').replace('hab.', '').strip()
        try:
            return int(rooms_str)
        except ValueError:
            return None
        
    def convert_floor_to_number(self, floor_str):
        floor_str = re.search(r'\d+', floor_str)

        if floor_str:
            floor_num = int(floor_str.group())
            return floor_num
        else:
            return 0
        
    def convert_lift_to_number(self, lift_str):
        if 'con ascensor' in lift_str:
            return 1
        elif 'sin ascensor' in lift_str:
            return 0
        else:
            return 2
        
    def extract_city(self, city_str):
        city = city_str.split(',')[-1].strip()
        return city

    def smooth_text(self, text):
        text = text.replace('\n', '')
        # Reemplazar múltiples espacios con uno solo y eliminar saltos de línea
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar espacios al principio y al final
        text = text.strip()
        
        return text
    
class PostgresPipeline:
    def open_spider(self, spider):
        #Este método se ejecuta cuando el spider se abre.
        #self.connection = psycopg2.connect(DATABASE_URL = os.getenv('DATABASE_URL'))
        self.connection = psycopg2.connect(
            host=spider.settings.get('POSTGRES_HOST'),
            port=spider.settings.get('POSTGRES_PORT'),
            dbname=spider.settings.get('POSTGRES_DB'),
            user=spider.settings.get('POSTGRES_USER'),
            password=spider.settings.get('POSTGRES_PASSWORD')
        )
        self.cursor = self.connection.cursor()

        # Crear la tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS propiedades (
                p_id INT PRIMARY KEY,
                nombre VARCHAR(255),
                fecha_idealista DATE,
                fecha_scraped DATE,
                precio INT,
                metros INT,
                habitaciones INT,
                planta INT,
                ascensor INT,
                poblacion VARCHAR(255),
                url VARCHAR(255),
                descripcion VARCHAR(4000)
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        # Cerrar la conexión cuando el spider se cierra
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        p_id = int(item['p_id'])
        print(f"p_id value being processed: {p_id}")

        try:
            # Verificar si el item ya existe en la base de datos
            self.cursor.execute("SELECT 1 FROM propiedades WHERE p_id = %s", (p_id,))
            result = self.cursor.fetchone()
            
            if result:
                # Si ya existe el registro, actualizamos el contenido
                print(f"Item already exists. Updating item: {p_id}")
                fecha_scraped = datetime.today().strftime('%Y-%m-%d')  # Fecha actual

                self.cursor.execute('''
                    UPDATE propiedades
                    SET nombre = %s,
                        fecha_idealista = %s,
                        fecha_scraped = %s,
                        precio = %s,
                        metros = %s,
                        habitaciones = %s,
                        planta = %s,
                        ascensor = %s,
                        poblacion = %s,
                        url = %s,
                        descripcion = %s
                    WHERE p_id = %s
                ''', (
                    item.get('nombre', 'Desconocido').capitalize(),
                    item.get('fecha_idealista'),
                    fecha_scraped,
                    item.get('precio'),
                    item.get('metros'),
                    item.get('habitaciones'),
                    item.get('planta'),
                    item.get('ascensor'),
                    item.get('poblacion'),
                    item.get('url'),
                    descripcion,  # Descripción procesada
                    p_id
                ))

            else:
                # Insertar un nuevo registro si no existe
                fecha_scraped = datetime.today().strftime('%Y-%m-%d')

                # Insert item into database
                self.cursor.execute("""
                    INSERT INTO propiedades (p_id, nombre, fecha_idealista, fecha_scraped, precio, metros, habitaciones, planta, ascensor, poblacion, url, descripcion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    p_id,
                    item.get('nombre'),
                    item.get('fecha_idealista'),
                    fecha_scraped,
                    item.get('precio'),
                    item.get('metros'),
                    item.get('habitaciones'),
                    item.get('planta'),
                    item.get('ascensor'),
                    item.get('poblacion'),
                    item.get('url'),
                    item.get('descripcion')
                ))

                # Confirmar cambios en la base de datos
                self.connection.commit()
                print(f"Item inserted successfully: {p_id}")

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            self.connection.rollback()
            raise DropItem(f"Database error: {e}")
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise DropItem(f"Unexpected error: {e}")

        return item
