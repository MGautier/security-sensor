# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-08 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0004_auto_20160116_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visualizations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Week_Month', models.IntegerField(verbose_name='Position of the week in a list. For calendar objects list')),
                ('Week_Day', models.IntegerField(verbose_name='Position of the day in a list. For calendar objects list')),
                ('Name_Day', models.IntegerField(verbose_name='Name of the day')),
                ('Date', models.DateField(verbose_name='Events process date')),
                ('Hour', models.TimeField(verbose_name='Events process hour')),
                ('Process_Events', models.IntegerField(verbose_name='Number of process events in a hour')),
            ],
        ),
    ]
