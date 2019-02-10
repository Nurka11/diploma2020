from django.contrib import admin
from .models import Item
from import_export.admin import ImportExportModelAdmin


def status_true(modeladmin, request, queryset):
    rows_updated = queryset.update(status='True')
    if rows_updated == 1:
        message_bit = "1 item was"
    else:
        message_bit = "%s items were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as True." % message_bit)


status_true.short_description = "Status -> True"


def status_false(modeladmin, request, queryset):
    rows_updated = queryset.update(status='False')
    if rows_updated == 1:
        message_bit = "1 item was"
    else:
        message_bit = "%s items were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as False." % message_bit)


status_false.short_description = "Status -> False"


class ItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id_product', 'name', 'price', 'categoryName', 'vendorName', 'status']
    ordering = ['name']
    actions = [status_true, status_false]
    fieldsets = [(None, {'fields': ['id_product', 'name', 'price', 'categoryName', 'vendorName', 'url']}),
                 ('Дополнительная информация', {'fields': ['status', 'categoryId', 'groupId'], 'classes': ['collapse']})]
    list_filter = ['status', 'categoryName', 'vendorName']
    search_fields = ['name']


admin.site.register(Item, ItemAdmin)
