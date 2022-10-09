import requests
from bs4 import BeautifulSoup
import csv

CSV = 'all_prod.csv'
HOST = 'https://ovk-term.ru'
URL = 'https://ovk-term.ru/kotli/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36 '
}



def get_html(url, params=''):  # получаем html сторiнку
    return requests.get(url, headers=HEADERS, params=params)    

def get_details_cities(html):
    soup = BeautifulSoup(html, 'html.parser')
    modal_data = soup.find("div", {"id": "stores-modal"})
    if not modal_data:
        return []
    modal_list = modal_data.find_all('li', class_='stores-item')
    cities = []
    city_prefix = 'г. Белгород'
    for el in modal_list:
        city_text = el.find('a').get_text(strip=True)
        if city_prefix in city_text:
            cities.append(city_text)
    return cities
    



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-wrap')
    all_products = []

    for item in items:
        item_url = item.find('div', class_='product-wrap__name').find('a').get('href')
        print(item_url)
        html_details = get_html(item_url).text
        cities = get_details_cities(html_details)
        if len(cities) == 0:
            continue

        all_products.append(
            {
                'title': item.find('div', class_='product-wrap__name').find('h3').get_text(strip=True),
                'url': item_url,
                'cost': item.find('li', class_='product-wrap__price-new').get_text(strip=True)
            }
        )
    return all_products


def save_csv(items, path):
    with open(path, 'w', newline='',  encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['url'], item['cost']])

def starter():
    pagination = input('Бля, брат, введи количество страниц: ')
    pagination = int(pagination.strip())
    html = get_html(URL)
    if html.status_code == 200:
        all_prod = []
        for page in range(1, pagination+1):
            print(f'Брат, собираю тебе новый айфон, снимаю все деньги с твоей карты: {page}')
            html = get_html(URL, params={'page': page})
            all_prod.extend(get_content(html.text))
            save_csv(all_prod, CSV)
        print('Все, пизда, денях нет')
    else:
        print('ERROR BRATAN')


starter()
