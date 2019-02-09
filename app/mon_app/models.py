from django.db import models

class Item(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=300, blank=True, null=True,)
    url = models.SlugField(verbose_name='Ссылка', max_length=300, unique=True)
    price = models.DecimalField(verbose_name='Цена', blank=True, null=True, max_digits=10, decimal_places=2)
    status = models.BooleanField(verbose_name='Статус', default=True)

    def __str__(self):
        return self.name
