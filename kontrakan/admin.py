# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class ProfilKontrakanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'lokasi', 'position_map', 'created', 'diupdate')

    def position_map(self, instance):
        if instance.lokasi is not None:
            return '<img src="http://maps.googleapis.com/maps/api/staticmap?center=%(latitude)s,%(longitude)s&zoom=%(zoom)s&size=%(width)sx%(height)s&maptype=roadmap&markers=%(latitude)s,%(longitude)s&sensor=false&visual_refresh=true&scale=%(scale)s" width="%(width)s" height="%(height)s">' % {
                'latitude': instance.lokasi.latitude,
                'longitude': instance.lokasi.longitude,
                'zoom': 15,
                'width': 500,
                'height': 200,
                'scale': 2
            }
    position_map.allow_tags = True

class KontrakanViewerAdmin(admin.ModelAdmin):
    list_display = ('user', 'kontrakan', 'timestamp',)

class FotoViewerAdmin(admin.ModelAdmin):
    list_display = ('kontrakan', 'foto_thumb', 'tanggal_upload',)

    def foto_thumb(self, instance):
        if instance.foto is not None:
            return '<img style="width: absolute; height: 140px;" src="http://127.0.0.1:8000/media/%(foto)s">' % {
                'foto': instance.foto,
            }

    foto_thumb.allow_tags = True

admin.site.register(ProfilKontrakan, ProfilKontrakanAdmin)
admin.site.register(Fasilitas)
admin.site.register(Administrasi)
