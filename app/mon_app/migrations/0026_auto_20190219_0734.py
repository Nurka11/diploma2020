# Generated by Django 2.1.5 on 2019-02-19 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0025_auto_20190219_0030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='id_product_my',
            new_name='id_product',
        ),
    ]
