# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-09 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0007_auto_20160209_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualizations',
            name='Name_Day',
            field=models.CharField(default='-', max_length=25),
        ),
    ]
