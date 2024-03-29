# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=40, unique=True)),
                ('payment_request_id', models.CharField(max_length=50)),
                ('shorturl', models.URLField()),
                ('longurl', models.URLField()),
                ('mac', models.CharField(max_length=60)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Started', 'Started'), ('Processing', 'Processing'), ('Payment Initiated', 'payment_initiated'), ('Payment Successful', 'payment_successful'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded'), ('Completed', 'Completed')], default='Started', max_length=120),
        ),
        migrations.AddField(
            model_name='paymentdetails',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
    ]
