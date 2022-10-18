import json
import requests


def fetch(url, params):
    headers = params['headers']
    if params['method'] == 'POST':
        return requests.post(url, headers=headers, data={'type': 'all'})


web_json = fetch("https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php", {
    "headers": {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "https://naturasiberica.ru/our-shops/",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "type=all",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
})

data = web_json.json()

def create_json(data):
    all_data = []
    for d in data['original']:
        data_magazine = {}

        data_magazine['address'] = d['address']
        data_magazine['lation'] = '-'
        data_magazine['name'] = d['name']
        data_magazine['phones'] = [d['phone']]

        if d['schedule'] == False:
            data_magazine['working_hours'] = '-'
        else:
            data_magazine['working_hours'] = [d['schedule']]

        all_data.append(data_magazine)

    for d in data['usual']:
        for cities in d['cities']:
            for mag in cities['shops']:
                data_magazine = {}

                data_magazine['address'] = mag['address']
                data_magazine['lation'] = [float(mag['location']['lag']), float(mag['location']['lng'])]
                data_magazine['name'] = mag['name']
                data_magazine['phones'] = [mag['phone']]

                all_data.append(data_magazine)
    return all_data



def save_data_json(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        try:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print('Сохранили json успешно')
        except Exception as e:
            print(f'Ошибка {e}')
save_data_json(create_json(data))
