# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-11-29 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20160504_1854'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='metatag',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='metatag',
            name='keywords',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='metatag',
            name='title',
            field=models.CharField(max_length=65),
        ),
    ]
