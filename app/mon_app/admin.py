from django.contrib import admin
from .models import CompetitorProduct, MyProduct, Match
from import_export.admin import ImportExportModelAdmin


def status_true(modeladmin, request, queryset):
    rows_updated = queryset.update(status='True')
    if rows_updated == 1:
        message_bit = "1 CompetitorsProduct was"
    else:
        message_bit = "%s CompetitorsProducts were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as True." % message_bit)


status_true.short_description = "Активный статус"


def status_false(modeladmin, request, queryset):
    rows_updated = queryset.update(status='False')
    if rows_updated == 1:
        message_bit = "1 CompetitorsProduct was"
    else:
        message_bit = "%s CompetitorsProducts were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as False." % message_bit)


status_false.short_description = "Неактивный статус"


def start_matching(modeladmin, request, queryset):
    modeladmin.message_user(request, "Объекты сравнены")


start_matching.short_description = "Сравнить"


class CompetitorsProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_product', 'name', 'price', 'categoryName', 'vendorName', 'shop', 'created', 'status')
    ordering = ['name']
    actions = [status_true, status_false, start_matching]
    fieldsets = [('Основная информация', {'fields': ['id_product', 'name', 'price', 'categoryName', 'vendorName', 'shop', 'url']}),
                 ('Дополнительная информация', {'fields': ['categoryId', 'groupId', 'status']})]
    list_filter = ['categoryName', 'shop', 'created', 'vendorName']
    search_fields = ['name']


class MyProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_product', 'name', 'price', 'categoryName', 'vendorName', 'created', 'status')
    ordering = ['name']
    actions = [status_true, status_false, start_matching]
    fieldsets = [('Основная информация', {'fields': ['id_product', 'name', 'price', 'categoryName', 'vendorName', 'url']}),
                 ('Дополнительная информация', {'fields': ['categoryId', 'groupId', 'status']})]
    list_filter = ['categoryName', 'created', 'vendorName']
    search_fields = ['name']


class MatchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_product_my', 'name_my', 'price_my', 'id_product_conc', 'name_conc', 'price_conc', 'diff', 'status', 'created')
    ordering = ['name_my']
    actions = [status_true, status_false]
    fieldsets = [('Первый товар', {'fields': ['id_product_my', 'name_my', 'price_my']}),
                 ('Второй товар', {'fields': ['id_product_conc', 'name_conc', 'price_conc']})]
    list_filter = ['created']
    search_fields = ['name_my']


admin.site.register(CompetitorProduct, CompetitorsProductAdmin)
admin.site.register(MyProduct, MyProductAdmin)
admin.site.register(Match, MatchAdmin)
