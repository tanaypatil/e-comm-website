# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20160428_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='payment_id',
            field=models.CharField(default='ABCD', max_length=40),
        ),
    ]
