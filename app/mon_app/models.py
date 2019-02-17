from django.db import models


class Item(models.Model):
    Mvideo = "Мвидео"
    Citilink = "Ситилинк"
    Wildberries = "Wildberries"
    shop_choices = ((Mvideo, 'Мвидео'), (Citilink, 'Ситилинк'), (Wildberries, 'Wildberries'))
    id_product = models.IntegerField('Артикул', blank=True, null=True)
    name = models.CharField('Имя', max_length=300, blank=True, null=True)
    price = models.DecimalField('Цена', blank=True, null=True, max_digits=10, decimal_places=2)
    categoryId = models.SlugField('ID категории', max_length=300, blank=True, null=True)
    categoryName = models.CharField('Категория', max_length=300, blank=True, null=True)
    vendorName = models.CharField('Производитель', max_length=300, blank=True, null=True)
    groupId = models.SlugField('ID группы', max_length=300, blank=True, null=True)
    url = models.SlugField('Ссылка', max_length=300, unique=True)
    status = models.BooleanField('Статус', default=True)
    shop = models.CharField('Магазин', max_length=30, blank=True, null=True, choices=shop_choices)
    created = models.DateTimeField('Дата', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
