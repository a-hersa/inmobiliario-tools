import os
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def scraper(url):
    encoded_url = requests.utils.quote(url, safe='')
    req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv("SCRAPINGANT")}&browser=false&proxy_country=ES'
    r = requests.get(req_url)
    soup = BeautifulSoup(r.text)
    nombre = soup.find('span', class_='main-info__title-main').text
    precio = soup.find('span', class_='info-data-price').text.replace('.','').strip(' €')
    metros = soup.find('div', class_='info-features').span.text.strip('\n').replace(' m²','')
    poblacion = soup.find('span', class_='main-info__title-minor').text.lower().split(", ")[-1].replace(" ", "").replace("'", "")
    datos = [nombre, precio, metros, unidecode(poblacion)]
    return datos