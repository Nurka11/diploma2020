from django.db import models


class CompetitorProduct(models.Model):
    Alser = "Alser"
    Sulpak = "Sulpak"
    Mechta = "Mechta"
    shop_choices = ((Alser, 'Alser'), (Sulpak, 'Sulpak'), (Mechta, 'Mechta'))
    name = models.CharField('Имя', max_length=300, blank=True, null=True)
    price = models.DecimalField('Цена', blank=True, null=True, max_digits=10, decimal_places=2)
    categoryId = models.SlugField('ID категории', max_length=300, blank=True, null=True)
    categoryName = models.CharField('Категория', max_length=300, blank=True, null=True)
    vendorName = models.CharField('Производитель', max_length=300, blank=True, null=True)
    groupId = models.SlugField('ID группы', max_length=300, blank=True, null=True)
    url = models.CharField('Ссылка', max_length=300, unique=True)
    status = models.BooleanField('Статус', default=True)
    shop = models.CharField('Магазин', max_length=30, blank=True, null=True, choices=shop_choices)
    created = models.DateTimeField('Дата', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар конкурента'
        verbose_name_plural = 'товары конкурента'


class MyProduct(models.Model):
    name = models.CharField('Имя', max_length=300, blank=True, null=True)
    price = models.DecimalField('Цена', blank=True, null=True, max_digits=10, decimal_places=2)
    categoryId = models.SlugField('ID категории', max_length=300, blank=True, null=True)
    categoryName = models.CharField('Категория', max_length=300, blank=True, null=True)
    vendorName = models.CharField('Производитель', max_length=300, blank=True, null=True)
    url = models.CharField('Ссылка', max_length=300, unique=True)
    status = models.BooleanField('Статус', default=True)
    created = models.DateTimeField('Дата', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'мой товар'
        verbose_name_plural = 'мои товары'


class Match(models.Model):
    Alser = "Alser"
    Sulpak = "Sulpak"
    Mechta = "Mechta"
    shop_choices = ((Alser, 'Alser'), (Sulpak, 'Sulpak'), (Mechta, 'Mechta'))
    name_my = models.CharField('Товар', max_length=300, blank=True, null=True)
    price_my = models.DecimalField('Моя цена', blank=True, null=True, max_digits=10, decimal_places=2)
    shop_competitor = models.CharField('Конкурент', max_length=30, blank=True, null=True, choices=shop_choices)
    name_competitor = models.CharField('Товар конкурента', max_length=300, blank=True, null=True)
    url = models.CharField('Ссылка', max_length=300, blank=True, null=True)
    price_competitor = models.DecimalField('Цена конкурента', blank=True, null=True, max_digits=10, decimal_places=2)
    diff = models.DecimalField('Разница', blank=True, null=True, max_digits=10, decimal_places=2, default='0')
    status = models.BooleanField('Моя цена ниже?', blank=True, null=True)
    created = models.DateTimeField('Дата сравнения', auto_now_add=True, blank=True, null=True,
                                   help_text="При добавлении нового сравнения вручную дата добавляется автоматически.")

    def __str__(self):
        id_product = 'Товар с артикулом {} : {}'.format(str(self.id), self.name_my)
        # id_product = 'Товар с артикулом ' + str(self.id_product) + ': ' + self.name_my
        return id_product

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'сравнение'
        verbose_name_plural = 'сравнения'
