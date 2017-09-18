# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from profiles.models import Profil
from ulasan.models import Rating
from django.db.models import Count, Avg
from kontrakan.models import (
	ProfilKontrakan,
	Fasilitas,
	Administrasi,
	BiayaTambahan,
	FotoKontrakan,
	Penghuni,
    KontarkanViewer
)
import string
import random
import arrow
import datetime

def search_view(request):
	lok = ProfilKontrakan.objects.all()
	data = []
	for l in lok:
		lat = l.lokasi.latitude
		lng = l.lokasi.longitude
		data.append({lat, lng})

	print(data)

	context = {
		"z_loc": data
	}
	return render(request, "search.html", context)

class LokasiData(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
    	lok = ProfilKontrakan.objects.all()
        data = []
        for l in lok:
        	data.append({
        		'lat': l.lokasi.latitude,
        		'lng': l.lokasi.longitude
        	})
        return Response(data)

class DetailKontrakan(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
    	ktr = ProfilKontrakan.objects.all()
        nama = []
        alamat = []
        kategori = []
        tersedia = []
        rating = []
        foto = []
        lokasi = []
        slug = []
        data = []
        # perbulan = []
        for k in ktr:
        	# nama.append(k.nama)
        	# alamat.append(k.alamat)
        	# kategori.append(k.get_kategori_display())
        	# slug.append(k.slug)
        	# tersedia.append(k.n_unit - k.n_penghuni)
        	# b = Administrasi.objects.get(kontrakan=k)
        	# perbulan.append()
        	# f = FotoKontrakan.objects.get(kontrakan=k,foto_utama=True)
        	# foto.append(f.foto.url)
        	# rating.append(Rating.objects.filter(kontrakan=k).aggregate(Avg('rating')))
        	# lokasi.append({"lat": k.lokasi.latitude,"lng": k.lokasi.longitude})

        	sisa = k.n_unit - k.n_penghuni
        	kat = k.get_kategori_display()
        	f = Fasilitas.objects.get(kontrakan=k)
        	b = Administrasi.objects.get(kontrakan=k)
        	g = FotoKontrakan.objects.filter(kontrakan=k,foto_utama=True)
        	if g.exists():
        		foto = g[0].foto.url
        	else:
        		foto = 'none'
        	r = Rating.objects.filter(kontrakan=k).aggregate(Avg('rating'))


        # data = {
        # 	"nama": nama,
        # 	"alamat": alamat,
        # 	"kategori": kategori,
        # 	"tersedia": tersedia,
        # 	"rating": rating,
        # 	"slug": slug,
        # 	"foto": foto,
        # 	"lokasi": lokasi,
        # }
        	data.append({
        		"nama": k.nama,
        		"alamat": k.alamat,
        		"kategori": kat,
        		"tersedia": sisa,
        		"rating": r,
        		"foto": foto,
        		"perbulan": float(b.per_bulan),
        		"lokasi": {"lat": k.lokasi.latitude,"lng": k.lokasi.longitude},
        		"slug": k.slug
        	})
        return Response(data)