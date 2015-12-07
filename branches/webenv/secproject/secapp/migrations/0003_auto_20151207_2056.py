# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-07 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0002_auto_20151207_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.CharField(max_length=100)),
                ('Timestamp_Insertion', models.CharField(max_length=100)),
                ('ID_Source', models.IntegerField()),
                ('Comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ip', models.CharField(max_length=60)),
                ('Hostname', models.CharField(max_length=60)),
                ('Tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LogSources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.TextField()),
                ('Type', models.CharField(max_length=100)),
                ('Model', models.CharField(max_length=255)),
                ('Active', models.SmallIntegerField()),
                ('Software_Class', models.CharField(max_length=50)),
                ('Path', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Macs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MAC', models.CharField(max_length=17)),
                ('TAG', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PacketAdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID_Tag', models.CharField(max_length=255)),
                ('Value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PacketEventsInformation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ID_IP_Source', models.IntegerField()),
                ('ID_IP_Dest', models.IntegerField()),
                ('ID_Source_Port', models.IntegerField()),
                ('ID_Dest_Port', models.IntegerField()),
                ('Protocol', models.CharField(max_length=20)),
                ('ID_Source_MAC', models.IntegerField()),
                ('ID_Dest_MAC', models.IntegerField()),
                ('RAW_Info', models.TextField()),
                ('TAG', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ports',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('Protocol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Service', models.CharField(max_length=60)),
                ('Description', models.CharField(max_length=100)),
                ('Tag', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TAG', models.CharField(max_length=255)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='libro',
            name='autores',
        ),
        migrations.RemoveField(
            model_name='libro',
            name='editor',
        ),
        migrations.DeleteModel(
            name='Autor',
        ),
        migrations.DeleteModel(
            name='Editor',
        ),
        migrations.DeleteModel(
            name='Libro',
        ),
    ]
