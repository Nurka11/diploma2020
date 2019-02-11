import requests
from bs4 import BeautifulSoup as BS


def get_html(url):
    r = requests.get(url)
    return r.text


def get_page_data(html):
    soup = BS(html, 'lxml')
    divs = soup.find_all('div', class_='catalog-item-inner catalog-product has-avails')
    for div in divs:
        id_product = div.find('div', class_='code').find_all('span')[1].text.strip()
        name = div.find('div', class_='title').find('a').find('h3').text.strip()
        price = div.find('div', class_='product-price').text.strip()

        print(price)


def main():
    sleep(5)
    url = 'https://www.dns-shop.ru/catalog/17a8ed0716404e77/domashnie-audiosistemy/?p=2'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
