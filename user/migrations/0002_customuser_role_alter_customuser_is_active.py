# Generated by Django 5.0.7 on 2024-08-01 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'admin'), ('seller', 'seller'), ('client', 'client')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
