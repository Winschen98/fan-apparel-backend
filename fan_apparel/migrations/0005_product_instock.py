# Generated by Django 3.2 on 2021-04-23 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fan_apparel', '0004_remove_product_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inStock',
            field=models.BooleanField(default=True),
        ),
    ]
