# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2017-01-14 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160419_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmetatag',
            name='description',
            field=models.CharField(max_length=160),
        ),
        migrations.AlterField(
            model_name='blogmetatag',
            name='keywords',
            field=models.CharField(max_length=160),
        ),
        migrations.AlterField(
            model_name='blogmetatag',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]