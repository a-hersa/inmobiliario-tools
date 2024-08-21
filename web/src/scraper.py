import os
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'es-ES,es;q=0.5',
    # 'cookie': 'smc="{}"; ISSESS53f9d0ba3b4062c86e11f9af46975bbf=NIVQh61mx7qDRWYOmakckcj5syT2g1pRk4nv82TnDoIwdwJJ; askToSaveAlertPopUp=true; userUUID=080b895c-1b4f-4e45-bb28-8efa1d0a57b5; uc="+L6rFntbSZeyHC9TaL9WbiuXTNx2yZT9mEQMBbJkMrzukom4Sf62aBBiDOv4Ld9M6Ee0gfwQMSMOXNxl6yRbBei+t973VYd6ArE+9p+I/YtgFSUMBJb86uEezkgLxQypJMCsrNYCoZOSckKZX8fvHg=="; nl="91g6yYYnLJGcb1gB3QVLpygk9J1yKj5u6urB7eeR/No/MaXRRa4xazq8It2Nf/ti8n7TufMezQLwY4MfPPWlccKzMb+20cqRKPv3Jq0/JVwASZubMplYNbIMWms69frhoJcjXYAKavk="; SESSION=ef256b4791da9513~4a3fd653-17ab-47c0-9953-c0a9734d58fa; utag_main__sn=72; utag_main_ses_id=1724163970818%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2F%3Bexp-1724167571467; utag_main__prevVtUrlReferrer=https://www.idealista.com/usuario/tus-alertas%3Bexp-1724167571467; utag_main__prevVtSource=Portal sites%3Bexp-1724167571467; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724167571467; utag_main__prevVtCampaignCode=%3Bexp-1724167571467; utag_main__prevVtCampaignLinkName=%3Bexp-1724167571467; utag_main__prevVtRecipientId=%3Bexp-1724167571467; utag_main__prevVtProvider=%3Bexp-1724167571467; utag_main__ss=0%3Bexp-session; utag_main__prevCompleteClickName=; contact4a3fd653-17ab-47c0-9953-c0a9734d58fa="{\'email\':\'XtyrNcg8bK7EvCKXWUXUtyR4ilq56QWwtkHUIo5zwy2CB+pdPhml/Q==\',\'name\':\'LyOA5/9IFC0=\',\'maxNumberContactsAllow\':10}"; cookieSearch-1="/venta-viviendas/premia-de-mar-barcelona/con-precio-hasta_120000,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,publicado_ultimas-48-horas,ultimas-plantas,plantas-intermedias/:1724164344364"; _last_search=officialZone; cc=eyJhbGciOiJIUzI1NiJ9.eyJjdCI6NjQyMjQ2NCwidXNlclByb2ZpbGVJZCI6NjQyMjQ2NCwiZXhwIjoxNzI0MjUxMzEwfQ.Jovob4IGzkQSycH_9N535Sw3WyHoH3SCv4EwVlYnjP0; utag_main__pn=6%3Bexp-session; datadome=TMiDvpjybvb2f5ytqF34cXVS4i~WGa9WslwCOvAridfP50W8QGuAtIJJSX9995nmnkiniQSo1BGOpTRqvNX9iaSVBVo2jxNpIAiJMD1htiicWMSwPtPtg6B1qn3j0DTZ; utag_main__se=10%3Bexp-session; utag_main__st=1724166712503%3Bexp-session; utag_main__prevCompletePageName=010-idealista/home > portal > viewLastSavedSearchModule%3Bexp-1724168512538; utag_main__prevLevel2=010-idealista/home%3Bexp-1724168512538',
    'priority': 'u=1, i',
    'referer': 'https://www.idealista.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

proxies = {
    'http': f'http://{os.getenv("PROXY")}' 
}

def scraper(url):
    # encoded_url = requests.utils.quote(url, safe='')
    # req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv("SCRAPINGANT")}&browser=false&proxy_country=ES'
    # print(req_url)
    # r = requests.get(req_url)
    r = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text)
    nombre = soup.find('span', class_='main-info__title-main').text
    precio = soup.find('span', class_='info-data-price').text.replace('.','').strip(' €')
    metros = soup.find('div', class_='info-features').span.text.strip('\n').replace(' m²','')
    poblacion = soup.find('span', class_='main-info__title-minor').text.lower().split(", ")[-1].replace(" ", "").replace("'", "")
    datos = [nombre, precio, metros, unidecode(poblacion)]
    return datos