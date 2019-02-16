import requests
import re

from bs4 import BeautifulSoup as BS


def get_html(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        return r.text
    print(r.status_code)


def get_page_data(html):
    soup = BS(html, 'lxml')

    category = soup.find_all('script')[-2]

    divs = soup.find_all('div', class_='dtList')
    for div in divs:
        id_product = div.find('div', class_='l_class').get('id').replace('c', '')
        name = div.find('div', class_='dtlist-inner-brand-name').find('span', class_='goods-name').text.strip()
        price = div.find('span', class_='price').text.strip().split('.')[0].replace(' руб', '').replace(' ', '')
        # categoryId =
        # categoryName =
        url = div.find('a', class_='ref_goods_n_p').get('href')
        vendorName = div.find('div', class_='dtlist-inner-brand-name').find('strong').text.strip().replace(' /', '')
        # print(url)
    print(category)


def main():
    url = 'https://www.wildberries.ru/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
