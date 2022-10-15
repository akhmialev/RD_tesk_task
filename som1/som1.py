import json
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

UA = UserAgent()
URL = 'https://som1.ru/shops/'
HEADERS = {'User-Agent': UA.random}

r = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(r.text, 'html.parser')

citys = soup.find('div', class_='col-xs-12 col-sm-6 citys-box').find_all('div', class_='col-xs-12 itjCitys')

IDS = []
for c in citys:
    city = c.find_all('label')
    for i in city:
        IDS.append(i.get('id'))

LINKS = []
for id in IDS:
    res = requests.get(url=URL, headers=HEADERS, cookies={'BITRIX_SM_CITY_ID': id})
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all('div', class_='shops-col shops-button')
    for l in links:
        link = l.find('a').get('href')
        LINKS.append(link)

DATA = []
count = 0
for l in LINKS:
    all_data = {}
    url = 'https://som1.ru' + l
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    address = soup.find('table').find_all('tr')
    name = soup.find('div', class_='page-body').find('h1').text

    data = []
    for a in address:
        data.append(a.find_all('td')[2].text)
    location = re.findall(r"\['(\d+\.\d+)','(\d+\.\d+)']", str(soup))

    all_data['address'] = data[0]
    all_data['lation'] = location
    all_data['name'] = name
    all_data['phones'] = [data[1]]
    all_data['working_hours'] = [data[2]]

    DATA.append(all_data)
    count += 1
    print(f'{count} - магазин записан')

with open('som1.json', 'w', encoding='utf-8') as file:
    json.dump(DATA, file, indent=4, ensure_ascii=False)
