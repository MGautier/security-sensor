# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-07 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0007_auto_20151207_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='ports',
            name='id_port',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
