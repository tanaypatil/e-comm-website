# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2017-02-12 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_users', '0007_auto_20170114_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='HowToUseVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('link', models.URLField()),
                ('description', models.CharField(max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
