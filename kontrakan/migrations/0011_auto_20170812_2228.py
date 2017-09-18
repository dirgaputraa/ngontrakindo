# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrakan', '0010_remove_profilkontrakan_id_kont'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fasilitas',
            name='parkir',
        ),
        migrations.AddField(
            model_name='fasilitas',
            name='parkir_mobil',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fasilitas',
            name='parkir_motor',
            field=models.BooleanField(default=False),
        ),
    ]
