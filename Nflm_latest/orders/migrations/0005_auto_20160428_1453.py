# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20160427_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='payment_id',
            field=models.CharField(default='ABC', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='payment_request_id',
            field=models.CharField(default='requestid', max_length=50),
        ),
    ]
