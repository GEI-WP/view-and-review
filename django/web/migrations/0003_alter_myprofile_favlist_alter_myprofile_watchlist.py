# Generated by Django 4.1.7 on 2023-05-11 18:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_myprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='favlist',
            field=models.TextField(default='', max_length=40000, validators=[django.core.validators.int_list_validator]),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='watchlist',
            field=models.TextField(default='', max_length=40000, validators=[django.core.validators.int_list_validator]),
        ),
    ]