# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 14:18
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20170805_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='avatar',
            field=versatileimagefield.fields.VersatileImageField(default='user-icon.jpg', upload_to='media/'),
        ),
    ]