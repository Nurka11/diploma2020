import requests
from bs4 import BeautifulSoup as BS
from .models import Item

from decimal import Decimal


def get_html(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
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
    soup = BS(html, 'lxml')
    divs = soup.find_all('a', class_="sel-product-tile-title")

    for div in divs:
        url = 'https://www.mvideo.ru' + div.get('href')
        products = div.get('data-product-info').split('{')[1::2]

        for product in products:
            refined_product = refined(product)
            p = '{' + refined_product

            dict = eval(p)

            id_product = dict.get('productId')
            name = dict.get('productName')
            price = dict.get('productPriceLocal')
            categoryId = dict.get('productCategoryId')
            categoryName = dict.get('productCategoryName')
            vendorName = dict.get('productVendorName')
            groupId = dict.get('productGroupId')

            data = {'id_product': id_product,
                    'name': name,
                    'price': price,
                    'categoryId': categoryId,
                    'categoryName': categoryName,
                    'vendorName': vendorName,
                    'groupId': groupId,
                    'url': url}

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
                id_product = int(item.get('id_product'))
                price = Decimal(item.get('price'))
                categoryId = item.get('categoryId')
                categoryName = item.get('categoryName')
                vendorName = item.get('vendorName')
                groupId = item.get('groupId')
            except TypeError:
                id_product = None
                price = None
                categoryId = None
                categoryName = None
                vendorName = None
                groupId = None
            name = item.get('name')
            _, created = Item.objects.update_or_create(url=url, defaults={'id_product': id_product,
                                                                          'name': name,
                                                                          'price': price,
                                                                          'categoryId': categoryId,
                                                                          'categoryName': categoryName,
                                                                          'vendorName': vendorName,
                                                                          'groupId': groupId,
                                                                          'status': True})
            if created:
                meta['created_count'] += 1
            else:
                meta['updated_count'] += 1
    return meta


def main():
    url_target = 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205'
    page_count = 10

    pattern = url_target + '/f/page={}'
    for i in range(1, page_count):
        url = pattern.format(str(i))
        html = get_html(url)
        product_list = get_page_data(html)
        meta = write_db(product_list)
        print(f'--> {i}: {meta}')


if __name__ == '__main__':
    main()
