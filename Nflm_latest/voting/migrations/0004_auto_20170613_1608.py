# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-13 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20170613_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairs',
            name='alt_1',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pairs',
            name='alt_2',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pairs',
            name='pid',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
