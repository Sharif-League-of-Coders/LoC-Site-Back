# Generated by Django 4.0.4 on 2022-05-24 20:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_home_created_alter_sponsor_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2022, 5, 24, 20, 53, 20, 962941), verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2022, 5, 24, 20, 53, 20, 962941), verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2022, 5, 24, 20, 53, 20, 962941), verbose_name='created'),
        ),
    ]
