# Generated by Django 5.0.7 on 2024-08-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_rename_products_sale_carts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='carts',
            field=models.ManyToManyField(blank=True, null=True, to='sales.productsale'),
        ),
    ]
