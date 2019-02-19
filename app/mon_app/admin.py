from django.contrib import admin
from .models import CompetitorProduct, MyProduct, Match
from import_export.admin import ImportExportModelAdmin


def status_true(modeladmin, request, queryset):
    rows_updated = queryset.update(status='True')
    if rows_updated == 1:
        message_bit = "1 Competitor`s products was"
    else:
        message_bit = "%s Competitor`s products were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as True." % message_bit)


def status_false(modeladmin, request, queryset):
    rows_updated = queryset.update(status='False')
    if rows_updated == 1:
        message_bit = "1 Competitor`s product was"
    else:
        message_bit = "%s Competitor`s products were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as False." % message_bit)


def start_matching_competitor(modeladmin, request, queryset):
    products_competitor = queryset.values('id_product', 'name', 'price', 'shop', 'url')

    for product_competitor in products_competitor:
        shop_competitor = product_competitor.get('shop')
        id_product_competitor = product_competitor.get('id_product')
        name_competitor = product_competitor.get('name')
        price_competitor = product_competitor.get('price')
        url_competitor = product_competitor.get('url')

        product_my = MyProduct.objects.filter(id_product=id_product_competitor).values('id_product', 'name', 'price')[0]
        id_product_my = product_my.get('id_product')
        name_my = product_my.get('name')
        price_my = product_my.get('price')

        diff = price_my - price_competitor

        if diff < 0:
            status = True
        elif diff > 0:
            status = False
        else:
            status = None

        Match.objects.update_or_create(id_product=id_product_competitor,
                                       defaults={'id_product': id_product_my,
                                                 'name_my': name_my,
                                                 'price_my': price_my,
                                                 'shop_competitor': shop_competitor,
                                                 'name_competitor': name_competitor,
                                                 'url': url_competitor,
                                                 'price_competitor': price_competitor,
                                                 'diff': diff,
                                                 'status': status
                                                 })
    modeladmin.message_user(request, "Объекты сравнены")


def start_matching_my(modeladmin, request, queryset):
    products_my = queryset.values('id_product', 'name', 'price')

    for product_my in products_my:
        id_product_my = product_my.get('id_product')
        name_my = product_my.get('name')
        price_my = product_my.get('price')

        product_competitor = CompetitorProduct.objects.filter(id_product=id_product_my).values('shop', 'id_product', 'name', 'price')[0]
        shop_competitor = product_competitor.get('shop')
        id_product_competitor = product_competitor.get('id_product')
        name_competitor = product_competitor.get('name')
        price_competitor = product_competitor.get('price')

        diff = price_my - price_competitor

        if diff < 0:
            status = True
        elif diff > 0:
            status = False
        else:
            status = None

        Match.objects.update_or_create(id_product=id_product_my,
                                       defaults={'id_product': id_product_competitor,
                                                 'name_my': name_my,
                                                 'price_my': price_my,
                                                 'shop_competitor': shop_competitor,
                                                 'name_competitor': name_competitor,
                                                 'price_competitor': price_competitor,
                                                 'diff': diff,
                                                 'status': status
                                                 })
    modeladmin.message_user(request, "Объекты сравнены")


class CompetitorsProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_product', 'name', 'price', 'categoryName', 'vendorName', 'shop', 'created', 'status')
    ordering = ['name']
    actions = [status_true, status_false, start_matching_competitor]
    fieldsets = [('Основная информация', {'fields': ['id_product', 'name', 'price', 'categoryName',
                                                     'vendorName', 'shop', 'url']}),
                 ('Дополнительная информация', {'fields': ['categoryId', 'groupId', 'status']})]
    list_filter = ['categoryName', 'shop', 'created', 'vendorName']
    search_fields = ['name', 'id_product']


class MyProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_product', 'name', 'price', 'categoryName', 'vendorName', 'created', 'status')
    ordering = ['name']
    actions = [status_true, status_false, start_matching_my]
    fieldsets = [('Основная информация', {'fields': ['id_product', 'name', 'price', 'categoryName', 'vendorName', 'url']}),
                 ('Дополнительная информация', {'fields': ['categoryId', 'status']})]
    list_filter = ['categoryName', 'created', 'vendorName']
    search_fields = ['name', 'id_product']


class MatchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_product', 'name_my', 'shop_competitor', 'name_competitor', 'price_my',
                    'price_competitor', 'diff', 'status', 'created')
    ordering = ['name_my']
    actions = []
    fieldsets = [('Артикул', {'fields': ['id_product']}),
                 ('Мой товар', {'fields': ['name_my', 'price_my']}),
                 ('Товар конкурента', {'fields': ['shop_competitor', 'url', 'name_competitor', 'price_competitor']})]
    list_filter = ['created', 'shop_competitor']
    search_fields = ['name_my', 'id_product']


status_true.short_description = "Активный статус"
status_false.short_description = "Неактивный статус"
start_matching_competitor.short_description = "Сравнить c моими товарами"
start_matching_my.short_description = "Сравнить c товарами конкурента"

admin.site.register(CompetitorProduct, CompetitorsProductAdmin)
admin.site.register(MyProduct, MyProductAdmin)
admin.site.register(Match, MatchAdmin)
