# Generated by Django 4.0.4 on 2022-05-16 20:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2022, 5, 16, 20, 27, 58, 273982), verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2022, 5, 16, 20, 27, 58, 273982), verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2022, 5, 16, 20, 27, 58, 273982), verbose_name='created'),
        ),
    ]
