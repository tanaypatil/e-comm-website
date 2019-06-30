# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customization',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='customization',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/customized/'),
        ),
    ]
