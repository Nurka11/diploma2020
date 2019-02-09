import requests
from bs4 import BeautifulSoup as BS
import csv


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def init_csv():
    with open('yamarket.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['id','name','url','price'])

def write_csv(data, index):
    with open('yamarket.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([index,
                         data['name'],
                         data['url'],
                         data['price']])


def refined(s):
    s1 = s.replace(' ', '')
    s2 = s1.replace('от ', '')
    s3 = s2.replace(' ₽', '')
    return s3


def get_page_data(html, index):
    soup = BS(html, 'lxml')
    # divs of items parsing
    divs = soup.find_all('div', class_="n-snippet-card2 i-bem b-zone b-spy-visible")
    for div in divs:
        index+=1

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

        write_csv(data, index)


def main():
    init_csv()
    index = 0
    pattern = 'https://market.yandex.ru/catalog--mobilnye-telefony/54726/list?hid=91491&page={}&onstock=1&local-offers-first=0&viewtype=list'
    # pattern = 'https://market.yandex.ru/catalog--umnye-chasy-i-braslety/56034/list?hid=10498025&page={}&onstock=1&local-offers-first=0'
    for i in range(1, 5):
        url = pattern.format(str(i))
        get_page_data(get_html(url), index)
        index+=48


if __name__ == '__main__':
    main()
