import json
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

ua = UserAgent()
URL = 'https://oriencoop.cl/sucursales.htm'
headers = {'User-Agent': ua.random}

r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

link = []
table = soup.find('div', class_='c-left')
magazine = table.find('ul', class_='c-list c-accordion').find_all('li')
for m in magazine:
    link.append(m.find('a').get('href'))

for l in link:
    if 'javascript:void(0);' == l:
        link.remove('javascript:void(0);')

datas = []
count = 0
for l in link:
    data = {}
    url = 'https://oriencoop.cl' + l
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    adress = soup.find('div', class_='s-dato').find('span').text
    name = soup.find('div', class_='s-dato').find('h3').text
    phone = soup.find('div', class_='s-dato').find_all('span')[1].text
    working_hours_manana = soup.find('div', class_='s-dato').find('img').next
    working_hours_tarde = soup.find('div', class_='s-dato').findAll('span')[4].text
    location = soup.find('div', class_='s-mapa').find('iframe').get('src')
    location = location.split('!')[5:7]
    location = location[0].replace('2d', ''), location[1].replace('3d', '')
    location = list(location)

    data['adress'] = adress
    data['lation'] = [float(location[0]), float(location[1])]
    data['name'] = name
    data['phones'] = [phone]
    data['working_hours'] = [working_hours_manana, working_hours_tarde]

    datas.append(data)
    count += 1
    print(f'{count}- локация')

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(datas, file, indent=4, ensure_ascii=False)
