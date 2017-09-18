# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 08:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilKontrakan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_kont', models.CharField(max_length=8)),
                ('nama', models.CharField(max_length=100)),
                ('lokasi', geoposition.fields.GeopositionField(max_length=42)),
                ('alamat', models.TextField(blank=True, null=True)),
                ('kategori', models.CharField(max_length=3)),
                ('subkat', models.CharField(max_length=5)),
                ('n_unit', models.IntegerField()),
                ('n_penghuni', models.IntegerField(default=0)),
                ('status', models.CharField(default='2', max_length=1)),
                ('deskripsi', models.TextField(blank=True, null=True)),
                ('verifikasi', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('pemilik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
