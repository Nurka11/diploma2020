from .models import MyProduct, CompetitorProduct, Match
from django.contrib import messages


def status_true_util(modeladmin, request, queryset):
    rows_updated = queryset.update(status='True')
    if rows_updated == 1:
        message_bit = "1 Competitor`s products was"
    else:
        message_bit = "%s Competitor`s products were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as True." % message_bit)


def status_false_util(modeladmin, request, queryset):
    rows_updated = queryset.update(status='False')
    if rows_updated == 1:
        message_bit = "1 Competitor`s product was"
    else:
        message_bit = "%s Competitor`s products were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as False." % message_bit)


def start_matching_competitor_util(modeladmin, request, queryset):
    products_competitor = queryset.values('id', 'name', 'price', 'shop', 'url')

    for product_competitor in products_competitor:
        shop_competitor = product_competitor.get('shop')
        name_competitor = product_competitor.get('name')
        price_competitor = product_competitor.get('price')
        url_competitor = product_competitor.get('url')

        product_my = MyProduct.objects.values('id', 'name', 'price')[0]
        name_my = product_my.get('name')
        price_my = product_my.get('price')

        diff = price_my - price_competitor

        if diff <= 0:
            status = True
        elif diff > 0:
            status = False
        obj, created = Match.objects.update_or_create(
            name_my=name_my, price_my=price_my, shop_competitor=shop_competitor, name_competitor=name_competitor,
            url=url_competitor, price_competitor=price_competitor, diff=diff, status=status
        )
    modeladmin.message_user(request, "Объекты сравнены")


def start_matching_my_util(modeladmin, request, queryset):
    products_my = queryset.values('id', 'name', 'price')

    for product_my in products_my:
        name_my = product_my.get('name')
        price_my = product_my.get('price')

        product_competitor = CompetitorProduct.objects.values('shop', 'id', 'name', 'price')[0]
        shop_competitor = product_competitor.get('shop')
        name_competitor = product_competitor.get('name')
        price_competitor = product_competitor.get('price')

        diff = price_my - price_competitor

        if diff < 0:
            status = True
        elif diff > 0:
            status = False
        else:
            status = None

        obj, created = Match.objects.update_or_create(
            name_my=name_my, price_my=price_my, shop_competitor=shop_competitor, name_competitor=name_competitor,
            price_competitor=price_competitor, diff=diff, status=status
        )

    modeladmin.message_user(request, "Объекты сравнены")


def analyze_util(modeladmin, request, queryset):
    count = queryset.count()
    prices_competitor = queryset.values('price_competitor')
    prices_my = queryset.values('price_my')

    sum_price_competitor = 0
    for price_competitor in prices_competitor:
        sum_price_competitor += price_competitor.get('price_competitor')

    sum_price_my = 0
    for price_my in prices_my:
        sum_price_my += price_my.get('price_my')

    avg_competitor = sum_price_competitor/count
    avg_my = sum_price_my/count
    if avg_my < avg_competitor:
        percent_diff = 100 - avg_my / avg_competitor * 100
        messages.info(request, "Средняя цена у конкурента: {}, средняя цена у меня: {}. Мои товары на {} процентов дешевле.".format(avg_competitor, avg_my, percent_diff))
    else:
        percent_diff = 100 - avg_competitor / avg_my * 100
        messages.error(request, "Средняя цена у конкурента: {}, средняя цена у меня: {}. Мои товары на {} процентов дороже.".format(avg_competitor, avg_my, percent_diff))
