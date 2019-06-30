# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-16 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_auto_20170614_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairs',
            name='a1',
            field=models.CharField(help_text='First Design submitted by.', max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pairs',
            name='a2',
            field=models.CharField(help_text='Second Design submitted by.', max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pairs',
            name='pid',
            field=models.CharField(help_text='ID of a pair. Should be unique integer and in order.', max_length=10, null=True, unique=True),
        ),
    ]