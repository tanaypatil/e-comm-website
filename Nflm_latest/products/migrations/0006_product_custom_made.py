# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-12-08 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161129_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='custom_made',
            field=models.BooleanField(default=False),
        ),
    ]
