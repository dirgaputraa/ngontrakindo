# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrakan', '0016_auto_20170814_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fasilitas',
            name='air',
            field=models.CharField(choices=[('1', 'PDAM(Masuk Biaya Sewa)'), ('2', 'PDAM(Di Luar Biaya Sewa)'), ('3', 'Pompa')], max_length=1),
        ),
        migrations.AlterField(
            model_name='fasilitas',
            name='listrik',
            field=models.CharField(choices=[('1', 'Masuk Biaya Sewa'), ('2', 'Di Luar Biaya Sewa')], max_length=1),
        ),
    ]
