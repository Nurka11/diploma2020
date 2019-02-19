from .utils import *
from django.contrib import admin
from .models import CompetitorProduct, MyProduct, Match
from import_export.admin import ImportExportModelAdmin
from django.urls import path
from django.http import HttpResponseRedirect


def status_true(modeladmin, request, queryset):
    status_true_util(modeladmin, request, queryset)


def status_false(modeladmin, request, queryset):
    status_false_util(modeladmin, request, queryset)


def start_matching_competitor(modeladmin, request, queryset):
    start_matching_competitor_util(modeladmin, request, queryset)


def start_matching_my(modeladmin, request, queryset):
    start_matching_my_util(modeladmin, request, queryset)


def save_graph_action(modeladmin, request, queryset):
    save_graph_util(modeladmin, request, queryset)


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
    list_display = ('id_product', 'name_my', 'shop_competitor', 'price_my',
                    'price_competitor', 'diff', 'status', 'created')
    ordering = ['name_my']
    actions = [save_graph_action]
    fieldsets = [('Артикул', {'fields': ['id_product']}),
                 ('Мой товар', {'fields': ['name_my', 'price_my']}),
                 ('Товар конкурента', {'fields': ['shop_competitor', 'url', 'name_competitor', 'price_competitor']})]
    list_filter = ['created', 'shop_competitor', 'status']
    search_fields = ['name_my', 'id_product']
    change_list_template = "mon_app/heroes_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('mortal/', self.set_mortal),
        ]
        return my_urls + urls

    def set_mortal(self, request):
        self.model.objects.all().update(status=False)
        self.message_user(request, "Анализ произведен")
        return HttpResponseRedirect("../")


status_true.short_description = "Активный статус"
status_false.short_description = "Неактивный статус"
start_matching_competitor.short_description = "Сравнить c моими товарами"
start_matching_my.short_description = "Сравнить c товарами конкурента"
save_graph_action.short_description = "Построить график"

admin.site.register(CompetitorProduct, CompetitorsProductAdmin)
admin.site.register(MyProduct, MyProductAdmin)
admin.site.register(Match, MatchAdmin)
