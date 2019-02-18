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


class Match(models.Model):
    id_product_my = models.IntegerField('Артикул MyShop', blank=True, null=True, unique=True)
    name_my = models.CharField('Имя MyShop', max_length=300, blank=True, null=True)
    price_my = models.DecimalField('Цена MyShop', blank=True, null=True, max_digits=10, decimal_places=2, unique=True)
    id_product_conc = models.IntegerField('Артикул конкурента', blank=True, null=True)
    name_conc = models.CharField('Имя конкурента', max_length=300, blank=True, null=True)
    price_conc = models.DecimalField('Цена конкурента', blank=True, null=True, max_digits=10, decimal_places=2)
    diff = models.DecimalField('Разница', blank=True, null=True, max_digits=10, decimal_places=2, default='0')
    status = models.BooleanField('Статус', default=True)
    created = models.DateTimeField('Дата сравнения', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name_my

    class Meta:
        verbose_name = 'сравнение'
        verbose_name_plural = 'сравнения'
