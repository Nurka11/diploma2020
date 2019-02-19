# Generated by Django 2.1.5 on 2019-02-18 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0014_match_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='id_product2',
            field=models.IntegerField(blank=True, null=True, verbose_name='Артикул'),
        ),
        migrations.AddField(
            model_name='match',
            name='name2',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='match',
            name='price2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена'),
        ),
    ]