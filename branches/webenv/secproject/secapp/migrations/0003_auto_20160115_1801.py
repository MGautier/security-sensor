# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0002_auto_20151216_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tcp',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='secapp.Ports')),
                ('Service', models.CharField(default='-', max_length=60)),
                ('Description', models.CharField(default='-', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Udp',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='secapp.Ports')),
                ('Service', models.CharField(default='-', max_length=60)),
                ('Description', models.CharField(default='-', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='ports',
            name='Description',
        ),
        migrations.RemoveField(
            model_name='ports',
            name='Protocol',
        ),
        migrations.RemoveField(
            model_name='ports',
            name='Service',
        ),
    ]
