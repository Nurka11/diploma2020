import requests
from bs4 import BeautifulSoup
from .models import Item
import os
from decimal import Decimal, InvalidOperation


def get_html(url):
    r = requests.get(url, headers={'User-Agent': os.environ['user_agent']})
    if r.ok:
        return r.text
    print(r.status_code)


def refined(s):
    s1 = s.replace('\t', '')
    s2 = s1.replace('\n', '')
    s3 = s2.replace('\r', '')
    return s3


def get_page_data(html):
    data_list = []
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find_all('div', class_='dtList')
    for div in divs:
        id_product = div.find('div', class_='l_class').get('id').replace('c', '')
        name = div.find('div', class_='dtlist-inner-brand-name').find('span', class_='goods-name').text.strip()
        price = div.find('span', class_='price').text.strip().split('.')[0].replace(' руб', '').replace(' ', '')
        categoryId = soup.find('div', class_='catalog-content').get('data-menu-id')
        categoryName = soup.find('div', class_='breadcrumbs').find_all('span')[-1].text.strip()
        url = div.find('a', class_='ref_goods_n_p').get('href')
        vendorName = div.find('div', class_='dtlist-inner-brand-name').find('strong').text.strip().replace(' /', '')
        shop = 'Wildberries'

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


def wildberries(url_target, page_count):
    pattern = url_target + '?page={}'
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
    wildberries()