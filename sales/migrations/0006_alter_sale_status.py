# Generated by Django 5.0.7 on 2024-08-03 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_sale_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('waiting', 'waiting'), ('preparing', 'preparing'), ('delivering', 'delivering'), ('delivered', 'delivered')], default='waiting', max_length=50),
        ),
    ]
