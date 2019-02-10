import requests
from bs4 import BeautifulSoup as BS
import csv
from .models import Item

from decimal import Decimal


def get_html(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        return r.text
    print(r.status_code)


def init_csv():
    with open('output/yamarket.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'url', 'price'])


def write_csv(data, index):
    with open('output/yamarket.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([index,
                         data['name'],
                         data['url'],
                         data['price']])


def write_db(items):
    meta = {'updated_count': 0, 'created_count': 0}
    urls = [item.get('url') for item in items if item.get('url')]
    Item.objects.filter(url__in=urls).update(status=False)

    for item in items:
        url = item.get('url')
        if url:
            try:
                price = Decimal(item.get('price'))
            except TypeError:
                price = None
            name = item.get('name')
            _, created = Item.objects.update_or_create(url=url, defaults={'name': name, 'price': price, 'status': True})
            if created:
                meta['created_count'] += 1
            else:
                meta['updated_count'] += 1
    return meta


def refined(s):
    s1 = s.replace(' ', '')
    s2 = s1.replace('от ', '')
    s3 = s2.replace(' ₽', '')
    return s3


def get_page_data(html, index):
    data_list = []
    soup = BS(html, 'lxml')
    # divs of items parsing
    divs = soup.find_all('div', class_="n-snippet-card2 i-bem b-zone b-spy-visible")
    for div in divs:
        index += 1

        # names and urls parsing
        divs_header = div.find_all('div', class_="n-snippet-card2__header")
        for div_header in divs_header:
            try:
                name = div_header.find('a').text
            except Exception:
                name = ''
            try:
                url = 'https://market.yandex.ru' + div_header.find('a').get('href')
            except Exception:
                url = ''
            data_header = {'name': name,
                           'url': url}

        # prices parsing
        divs_price = div.find_all('div', class_="n-snippet-card2__main-price-wrapper")
        for div_price in divs_price:
            try:
                p = div_price.find('a').text
                price = refined(p)
            except Exception:
                price = ''
            data_price = {'price': price}

        # colecting in one dict.
        data = {'name': data_header['name'],
                'url': data_header['url'],
                'price': data_price['price']}

        data_list.append(data)
    return data_list


def main():
    init_csv()
    index = 0
    pattern = 'https://market.yandex.ru/catalog--mobilnye-telefony/54726/list?hid=91491&page={}&onstock=1&local-offers-first=0&viewtype=list'

    for i in range(1, 5):
        url = pattern.format(str(i))
        html = get_html(url)
        product_list = get_page_data(html, index)
        meta = write_db(product_list)
        print(f'--> {i}: {meta}')
        # get_page_data(get_html(url), index)
        index += 48


if __name__ == '__main__':
    main()
