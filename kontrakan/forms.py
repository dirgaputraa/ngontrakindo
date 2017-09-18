# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from .models import *
from django.core.files import File
from PIL import Image


class KontrakanEditForm(forms.ModelForm):
	n_unit = forms.IntegerField(
		label='Jumlah Unit yang Dikontrakan',
		help_text='Khusus kontrakan rumah hanya 1 unit. Selain itu, lebih dari 1 unit.'
	)
	n_penghuni = forms.IntegerField(
		label='Jumlah Penghuni Kontrakan/Kost Saat Ini'
	)
	KAT = (
		('1', 'Kontrakan Rumah'),
		('2', 'Kontrakan Petakan'),
		('3', 'Kost Putra'),
		('4', 'Kost Putri'),
		('5', 'Kost Campur'),
	)
	# kategori = forms.ChoiceField(choices=KAT,widget=forms.RadioSelect(attrs={'disabled':'disabled'}))
	class Meta:
		model = ProfilKontrakan
		fields = [
			'nama',
			'alamat',
			'kategori',
			'n_unit',
			'n_penghuni',
			'status',
			'deskripsi',
			]

	def clean(self, *args, **kwargs):
		return super(KontrakanEditForm, self).clean(*args, **kwargs)


class KontrakanForm(forms.ModelForm):
	nama = forms.CharField(label='Nama Kontrakan/Kost',help_text='Misal: Melati, Griya Indah, atau nama pemilik seperti H. Rojali, Kesya, dsb.')
	KAT = (
		('1', 'Kontrakan Rumah'),
		('2', 'Kontrakan Petakan'),
		('3', 'Kost Putra'),
		('4', 'Kost Putri'),
		('5', 'Kost Campur'),
	)
	kategori = forms.ChoiceField(choices=KAT,widget=forms.RadioSelect())
	n_unit = forms.IntegerField(
		label='Jumlah Unit yang Dikontrakan',
		help_text='Khusus kontrakan rumah hanya 1 unit. Selain itu, lebih dari 1 unit.'
	)
	n_penghuni = forms.IntegerField(
		label='Jumlah Penghuni Kontrakan/Kost Saat Ini'
	)
	STATUS = (
		('1', 'Sedang Dibangun'),
		('2', 'Siap Huni'),
		('3', 'Sedang Renovasi'),
	)
	status = forms.ChoiceField(
		choices=STATUS,
		widget=forms.RadioSelect(),
		label='Status Kontrakan Saat Ini',
		help_text='Kontrakan Anda akan kami kondisikan tidak dapat menerima penghuni saat status kontrakan Sedang Dibangun/Renovasi'
	)
	alamat = forms.CharField(
		label='Alamat Lengkap',
		widget=forms.Textarea(attrs={'placeholder': 'Nama jalan/gang, RT/RW, Kelurahan, Kecamatan, Kota, Provinsi'})
	)
	deskripsi = forms.CharField(
		label='Deskripsi Kontrakan',
		widget=forms.Textarea(attrs={'placeholder': 'Penjelasan singkat tentang kontrakan Anda'})
	)
	class Meta:
		model = ProfilKontrakan
		fields = [
			'lokasi',
			'alamat',
			'kategori',
			'nama',
			'n_unit',
			'n_penghuni',
			'status',
			'deskripsi',
			]

	def clean(self, *args, **kwargs):
		return super(KontrakanForm, self).clean(*args, **kwargs)

class FasilitasForm(forms.ModelForm):
	luas = forms.CharField(label='Luas Kontrakan(meter)',help_text='Misal: 8x5')
	LIS = (
		('1', 'Masuk Biaya Sewa'),
		('2', 'Di Luar Biaya Sewa'),
	)
	listrik = forms.ChoiceField(choices=LIS,widget=forms.RadioSelect())
	AIR = (
		('1', 'PDAM(Masuk Biaya Sewa)'),
		('2', 'PDAM(Di Luar Biaya Sewa)'),
		('3', 'Pompa'),
	)
	air = forms.ChoiceField(choices=AIR,widget=forms.RadioSelect())
	class Meta:
		model = Fasilitas
		fields = [
			'luas',
			'listrik',
			'air',
			'kasur',
			'lemari',
			'tv',
			'ac',
			'wifi',
			'kamar_mandi_dalam',
			'kamar_mandi_luar',
			'kloset_duduk',
			'kloset_jongkok',
			'shower',
			'wastafel',
			'dapur',
			'laundry',
			'jemuran',
			'parkir_mobil',
			'parkir_motor',
			'gerbang',
			'satpam',
			'cctv',
			'rumah_sakit',
			'rumah_makan',
			'pasar',
			'mall',
			'mini_market',
			'stasiun',
			'terminal_bus',
			'akses_tol',
			'fasilitas_lain',
			]

	def clean(self, *args, **kwargs):
		return super(FasilitasForm, self).clean(*args, **kwargs)

class AdministrasiForm(forms.ModelForm):
	class Meta:
		model = Administrasi
		fields = [
			'penghuni_max',
			'harian',
			'per_hari',
			'mingguan',
			'per_minggu',
			'bulanan',
			'per_bulan',
			'tahunan',
			'per_tahun',
			'denda',
			'biaya_lain',
			'syarat_ketentuan',
		]

	def clean(self, *args, **kwargs):
		return super(AdministrasiForm, self).clean(*args, **kwargs)


class GaleriForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = FotoKontrakan
        fields = ('foto', 'x', 'y', 'width', 'height', )

class PenghuniForm(forms.ModelForm):
	class Meta:
		model = Penghuni
		fields = ('user', 'kontrakan','aktif','konfirm','tanggal_masuk')

class DaftarForm(forms.ModelForm):
	domain = forms.CharField(
		label='Domain Kontrakan',
		help_text='Tulis domain sesuai nama kontrakan dan tanpa spasi, misal: kontrakanmelati. Domain ini akan digunakan untuk mengakses aplikasi kontrakan Anda.'
	)
	class Meta:
		model = Daftar
		fields = ('domain',)

