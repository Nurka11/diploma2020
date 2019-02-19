# Generated by Django 2.1.5 on 2019-02-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0024_auto_20190219_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitorproduct',
            name='url',
            field=models.CharField(max_length=300, unique=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.BooleanField(blank=True, null=True, verbose_name='Моя цена ниже?'),
        ),
        migrations.AlterField(
            model_name='myproduct',
            name='url',
            field=models.CharField(max_length=300, unique=True, verbose_name='Ссылка'),
        ),
    ]