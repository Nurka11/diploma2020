from django.db import models


class Item(models.Model):
    Mvideo = "M"
    Citilink = "C"
    Wildberries = "W"
    shop_choices = ((Mvideo, 'Мвидео'), (Citilink, 'Ситилинк'), (Wildberries, 'Wildberries'))
    id_product = models.IntegerField(verbose_name='Артикул', blank=True, null=True)
    name = models.CharField(verbose_name='Имя', max_length=300, blank=True, null=True)
    price = models.DecimalField(verbose_name='Цена', blank=True, null=True, max_digits=10, decimal_places=2)
    categoryId = models.SlugField(verbose_name='ID категории', max_length=300, blank=True, null=True)
    categoryName = models.CharField(verbose_name='Категория', max_length=300, blank=True, null=True)
    vendorName = models.CharField(verbose_name='Производитель', max_length=300, blank=True, null=True)
    groupId = models.SlugField(verbose_name='ID группы', max_length=300, blank=True, null=True)
    url = models.SlugField(verbose_name='Ссылка', max_length=300, unique=True)
    status = models.BooleanField(verbose_name='Статус', default=True)
    shop = models.CharField(verbose_name='Магазин', max_length=30, blank=True, null=True, choices=shop_choices)
    created = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
