import requests
from bs4 import BeautifulSoup
from mon_app.models import CompetitorProduct
import json
from decimal import Decimal
from random import uniform


class HttpException(Exception):
    pass


def get_html(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        return r.text
    else:
        exp = HttpException()
        exp.status_code = r.status_code
        raise exp


def get_page_data(html):
    alser = []
    soup = BeautifulSoup(html, 'html.parser')  # dlya togo 4tobi izvlech dannye iz DOM tree of our site
    items = soup.find_all('div', class_='good-item-in')
    category = soup.find_all('h1', class_='page-title')

    for item in items:
        print()
        for cat in category:
            for stat in item.find('div', class_='good-item-title text--black')('a'):
                v = stat['href']
            alser.append({
                'name': item.find('div', class_='good-item-title text--black').get_text(),
                'categoryName': cat.find('span', class_='title-2').get_text(),
                'price': "".join(item.find('strong', class_='text--black').get_text().split()),
                'url':  'https://alser.kz/{}'.format(v),
                'shop': 'Alser',
            })
    return alser


def write_db(competitor_products):
    meta = {'updated_count': 0, 'created_count': 0}
    # urls = [competitor_product.get('url') for competitor_product in competitor_products if competitor_product.get('url')]
    # CompetitorProduct.objects.filter(url__in=urls).update(status=False)

    for competitor_product in competitor_products:
        url = competitor_product.get('url')

        # if url:
        price = Decimal(competitor_product.get('price'))
        # categoryId = competitor_product.get('categoryId')
        categoryName = competitor_product.get('categoryName')
        # vendorName = competitor_product.get('vendorName')
        # groupId = competitor_product.get('groupId')
        shop = competitor_product.get('shop')
        name = competitor_product.get('name')

        _, created = CompetitorProduct.objects.update_or_create(url=url, defaults={
                                                                                   'name': name,
                                                                                   'price': price,
                                                                                   # 'categoryId': categoryId,
                                                                                   'categoryName': categoryName,
                                                                                   # 'vendorName': vendorName,
                                                                                   # 'groupId': groupId,
                                                                                   'status': True,
                                                                                   'shop': shop})
        if created:
            meta['created_count'] += 1
        else:
            meta['updated_count'] += 1
    return meta


def alser(url_target, page_count):
    pattern = url_target + '?page={}'
    for i in range(1, int(page_count) + 1):
        url = pattern.format(str(i))
        html = get_html(url)
        product_list = get_page_data(html)
        write_db(product_list)
        product_count_on_page = len(product_list)
        print("-" * 42)
        print("На странице номер {} получено {} продуктов".format(i, product_count_on_page))
        print("-" * 42)
        meta = write_db(product_list)
        print(f'--> {i}: {meta}')
    all_product_count = int(product_count_on_page) * int(page_count)
    print("Всего на странице {} получено {} продуктов".format(url_target, all_product_count))
    print("Парсинг завершен")
