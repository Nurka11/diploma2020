import requests
from bs4 import BeautifulSoup as BS
from .models import Item
import json
from decimal import Decimal, InvalidOperation


class HttpException2(Exception):
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
    data_list = []
    soup = BS(html, 'lxml')
    divs = soup.find_all('div', class_='subcategory-product-item')

    for div in divs:
        json_product = div.get('data-params')
        url = div.find('a', class_='link_gtm-js link_pageevents-js ddl_product_link').get('href')
        data = json.loads(json_product)

        id_product = data.get('id')
        categoryId = data['categoryId']
        price = data['price']
        name = data['shortName']
        categoryName = data['categoryName']
        vendorName = data['brandName']
        shop = 'Ситилинк'

        data = {'id_product': id_product,
                'name': name,
                'price': price,
                'categoryId': categoryId,
                'categoryName': categoryName,
                'vendorName': vendorName.lower().title(),
                'url': url,
                'shop': shop}

        print(data)
        data_list.append(data)
    return data_list


def write_db(items):
    meta = {'updated_count': 0, 'created_count': 0}
    urls = [item.get('url') for item in items if item.get('url')]
    Item.objects.filter(url__in=urls).update(status=False)

    for item in items:
        url = item.get('url')
        if url:
            try:
                price = Decimal(item.get('price'))
            except InvalidOperation:
                price = None
            try:
                id_product = int(item.get('id_product'))
            except ValueError:
                id_product = None

            categoryId = item.get('categoryId')
            categoryName = item.get('categoryName')
            vendorName = item.get('vendorName')
            groupId = item.get('groupId')
            shop = item.get('shop')
            name = item.get('name')

            _, created = Item.objects.update_or_create(url=url, defaults={'id_product': id_product,
                                                                          'name': name,
                                                                          'price': price,
                                                                          'categoryId': categoryId,
                                                                          'categoryName': categoryName,
                                                                          'vendorName': vendorName,
                                                                          'groupId': groupId,
                                                                          'status': True,
                                                                          'shop': shop})
            if created:
                meta['created_count'] += 1
            else:
                meta['updated_count'] += 1
    return meta


def citilink(url_target, page_count):
    pattern = url_target + '/?p={}'
    for i in range(1, int(page_count) + 1):
        url = pattern.format(str(i))
        html = get_html(url)
        product_list = get_page_data(html)
        write_db(product_list)
        product_count_on_page = len(product_list)
        print("-" * 42 + "\nНа странице номер {} получено {} продуктов".format(i, product_count_on_page) + "\n" + "-" * 42)
        meta = write_db(product_list)
        print(f'--> {i}: {meta}')
    all_product_count = int(product_count_on_page) * int(page_count)
    print("-" * 42 + "\nВсего на странице {} получено {} продуктов".format(url_target, all_product_count) + "\n" + "-" * 42)


if __name__ == '__main__':
    citilink()
