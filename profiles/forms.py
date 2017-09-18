# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from .models import Profil, Medsos
from django.core.files import File
from PIL import Image
import datetime

User = get_user_model()

class Nama(forms.ModelForm):
	first_name = forms.CharField(label='Nama Depan')
	last_name = forms.CharField(label='Nama Belakang')
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name'
			]

	def __init__(self, *args, **kwargs):
		return super(Nama, self).__init__(*args, **kwargs)

class ProfilForm(forms.ModelForm):
	tgl_lahir = forms.DateField(
		widget=forms.TextInput(
			attrs={'type': 'date','min': '1900-01-01','max': datetime.datetime.now().date()}
		), label='Tanggal Lahir'
	)
	JK = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
	jk = forms.ChoiceField(label='Jenis Kelamin',choices=JK,widget=forms.RadioSelect())
	alamat = forms.CharField(label='Alamat Lengkap', widget=forms.Textarea)
	no_telp = forms.CharField(label='No. Telepon')
	instansi = forms.CharField(label='Instansi')
	class Meta:
		model = Profil
		fields = [
			'tgl_lahir',
			'jk',
			'alamat',
			'no_telp',
			'profesi',
			'instansi'
			]

	def __init__(self, *args, **kwargs):
		return super(ProfilForm, self).__init__(*args, **kwargs)
		

class AvatarForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profil
        fields = ('avatar', 'x', 'y', 'width', 'height', )


class UserForm(forms.ModelForm):
	first_name = forms.CharField(label='Nama Depan')
	last_name = forms.CharField(label='Nama Belakang')
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'username',
			]

	def __init__(self, *args, **kwargs):
		return super(UserForm, self).__init__(*args, **kwargs)


class MedsosForm(forms.ModelForm):
	class Meta:
		model = Medsos
		fields = [
			'facebook',
			'twitter',
			'instagram',
			]

	def __init__(self, *args, **kwargs):
		return super(MedsosForm, self).__init__(*args, **kwargs)