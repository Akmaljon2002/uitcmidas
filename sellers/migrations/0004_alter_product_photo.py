# Generated by Django 5.0.7 on 2024-08-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
