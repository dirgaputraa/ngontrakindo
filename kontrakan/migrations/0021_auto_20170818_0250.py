# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrakan', '0020_auto_20170818_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilkontrakan',
            name='diupdate',
            field=models.DateTimeField(),
        ),
    ]
