# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-07 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0004_auto_20151207_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ports',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
