# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-12-07 12:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managing_users', '0004_auto_20161207_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customization',
            name='timestamp',
        ),
    ]
