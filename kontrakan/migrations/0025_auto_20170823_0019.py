# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrakan', '0024_auto_20170820_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilkontrakan',
            name='kategori',
            field=models.CharField(choices=[('1', 'Kontrakan Rumah'), ('2', 'Kontrakan Petakan'), ('3', 'Kost Putra'), ('4', 'Kost Putri'), ('5', 'Kost Campur')], max_length=3),
        ),
    ]
