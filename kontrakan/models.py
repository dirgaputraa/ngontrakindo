# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from geoposition.fields import GeopositionField
from django.utils.encoding import python_2_unicode_compatible
from versatileimagefield.fields import VersatileImageField
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from .utils import unique_slug_generator


@python_2_unicode_compatible
class ProfilKontrakan(models.Model):
	nama = models.CharField(max_length=100,null=False,blank=False)
	pemilik = models.ForeignKey(User,null=False,blank=False)
	lokasi = GeopositionField()
	alamat = models.TextField(blank=True,null=True)
	KAT = (
		('1', 'Kontrakan Rumah'),
		('2', 'Kontrakan Petakan'),
		('3', 'Kost Putra'),
		('4', 'Kost Putri'),
		('5', 'Kost Campur'),
	)
	kategori = models.CharField(max_length=3,choices=KAT,null=False,blank=False)
	SUB = (
		('RMH', 'Rumah'),
		('PTK', 'Petakan'),
	)
	n_unit = models.IntegerField(null=False,blank=False,default=1)
	n_penghuni = models.IntegerField(null=False,blank=False,default=0)
	STATUS = (
		('1', 'Sedang Dibangun'),
		('2', 'Siap Huni'),
		('3', 'Sedang Renovasi'),
	)
	status = models.CharField(max_length=1,choices=STATUS,null=False,blank=False,default='2')
	deskripsi = models.TextField(blank=True,null=True)
	verifikasi = models.BooleanField(default=False)
	ratings = GenericRelation(Rating, related_query_name='profilkontrakans')
	slug = models.SlugField(blank=True,null=True)
	dilihat = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)
	diupdate = models.DateTimeField(auto_now=False,blank=True,null=True)

	def __str__(self):
		return self.nama

def kontrakan_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(kontrakan_pre_save_receiver, sender=ProfilKontrakan)


@python_2_unicode_compatible
class KontarkanViewer(models.Model):
	user = models.CharField(max_length=80);
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.kontrakan.nama

		
@python_2_unicode_compatible
class Fasilitas(models.Model):
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	luas = models.CharField(max_length=7)
	LIS = (
		('1', 'Masuk Biaya Sewa'),
		('2', 'Di Luar Biaya Sewa'),
	)
	listrik = models.CharField(max_length=1,choices=LIS)
	AIR = (
		('1', 'PDAM(Masuk Biaya Sewa)'),
		('2', 'PDAM(Di Luar Biaya Sewa)'),
		('3', 'Pompa'),
	)
	air = models.CharField(max_length=1,choices=AIR)
	tv = models.BooleanField(default=False)
	kasur = models.BooleanField(default=False)
	lemari = models.BooleanField(default=False)
	ac = models.BooleanField(default=False)
	wifi = models.BooleanField(default=False)
	kamar_mandi_dalam = models.BooleanField(default=False)
	kamar_mandi_luar = models.BooleanField(default=False)
	kloset_jongkok = models.BooleanField(default=False)
	kloset_duduk = models.BooleanField(default=False)
	wastafel = models.BooleanField(default=False)
	shower = models.BooleanField(default=False)
	dapur = models.BooleanField(default=False)
	laundry = models.BooleanField(default=False)
	jemuran = models.BooleanField(default=False)
	parkir_mobil = models.BooleanField(default=False)
	parkir_motor = models.BooleanField(default=False)
	gerbang = models.BooleanField(default=False)
	satpam = models.BooleanField(default=False)
	cctv = models.BooleanField(default=False)
	pasar = models.BooleanField(default=False)
	mall = models.BooleanField(default=False)
	rumah_sakit = models.BooleanField(default=False)
	rumah_makan = models.BooleanField(default=False)
	mini_market = models.BooleanField(default=False)
	terminal_bus = models.BooleanField(default=False)
	stasiun = models.BooleanField(default=False)
	akses_tol = models.BooleanField(default=False)
	fasilitas_lain = models.TextField(null=True,blank=True)

	def __str__(self):
		return self.kontrakan.nama

@python_2_unicode_compatible
class Administrasi(models.Model):
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	harian = models.BooleanField(default=False)
	per_hari = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	mingguan = models.BooleanField(default=False)
	per_minggu = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	bulanan = models.BooleanField(default=False)
	per_bulan = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	tahunan = models.BooleanField(default=False)
	per_tahun = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	denda = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	syarat_ketentuan = models.TextField(blank=True,null=True)
	penghuni_max = models.IntegerField(default=1)
	biaya_lain = models.BooleanField(default=False)

	def __str__(self):
		return self.kontrakan.nama

@python_2_unicode_compatible
class BiayaTambahan(models.Model):
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	nama_biaya = models.CharField(max_length=50,null=True,blank=True)
	nominal = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	keterangan = models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return self.kontrakan.nama

@python_2_unicode_compatible
class Penghuni(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	aktif = models.BooleanField(default=False)
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	konfirm = models.BooleanField(default=False)
	tanggal_masuk = models.DateTimeField(null=True,blank=True)
	tanggal_keluar = models.DateTimeField(null=True,blank=True)
	ket = models.CharField(max_length=15,null=True,blank=True)

	def __str__(self):
		return self.ket
		
@python_2_unicode_compatible
class FotoKontrakan(models.Model):
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	foto = VersatileImageField(upload_to = 'kontrakan/',null=True,blank=True)
	tanggal_upload = models.DateTimeField(auto_now_add=True)
	foto_utama = models.BooleanField(default=False)

	def __str__(self):
		return self.kontrakan.nama

@python_2_unicode_compatible
class Pengurus(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE,null=True,blank=True)
	edit_kontrakan = models.BooleanField(default=False)
	konfirm_penghuni = models.BooleanField(default=False)
	transaksi = models.BooleanField(default=False)
	galeri = models.BooleanField(default=False)
	ulasan = models.BooleanField(default=False)

	def __str__(self):
		return self.kontrakan.nama


# @python_2_unicode_compatible
class Transaksi(models.Model):
	biaya = MoneyField(max_digits=8,decimal_places=2,default_currency='IDR',null=True,blank=True)
	penghuni = models.ForeignKey(Penghuni, on_delete=models.CASCADE)
	keterangan = models.CharField(max_length=50,null=True,blank=True)
	pj = models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return self.keterangan


class Daftar(models.Model):
	pemilik = models.ForeignKey(User,null=False,blank=False)
	domain = models.CharField(max_length=50,null=True,blank=True)
	tanggal_daftar = models.DateTimeField(auto_now_add=True)
	proses = models.BooleanField(default=False)

	def __str__(self):
		return self.pemilik.username