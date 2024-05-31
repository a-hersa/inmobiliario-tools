import os
import requests
from bs4 import BeautifulSoup

def scraper(url):
    encoded_url = requests.utils.quote(url, safe='')
    req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv("SCRAPINGANT")}&browser=false&proxy_country=ES'
    r = requests.get(req_url)
    soup = BeautifulSoup(r.text)
    nombre = soup.find('span', class_='main-info__title-main').text
    precio = soup.find('span', class_='info-data-price').text.replace('.','').strip(' €')
    metros = soup.find('div', class_='info-features').span.text.strip('\n').replace(' m²','')
    datos = [nombre, precio, metros]
    return datos