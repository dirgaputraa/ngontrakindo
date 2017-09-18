# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from versatileimagefield.fields import VersatileImageField

@python_2_unicode_compatible
class Profil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tgl_lahir = models.DateField(blank=True,null=True)
	JK = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
	jk = models.CharField(max_length=1, choices=JK)
	alamat = models.TextField(blank=True,null=True)
	no_telp = models.CharField(max_length=20,blank=True,null=True)
	PRO = (
    	('PNS', 'Pegawai Negri'),
    	('PSW', 'Pegawai Swasta'),
    	('PDG', 'Pedagang'),
    	('PSH', 'Pengusaha'),
    	('DRV', 'Driver'),
    	('MHS', 'Mahasiswa'),
    )
	profesi = models.CharField(max_length=3, choices=PRO, null=True)
	instansi = models.CharField(max_length=80,null=True,blank=True)
	TYPE = (
        ('1', 'Pemilik'),
        ('2', 'Pengurus'),
        ('3', 'Penghuni'),
    )
	user_type = models.CharField(max_length=1, choices=TYPE, default='3')
	avatar = VersatileImageField(upload_to = 'media/', default = 'user-icon.jpg')
	n_login = models.IntegerField(default=1)

	def __str__(self):
		return self.user.username


@python_2_unicode_compatible
class Medsos(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	facebook = models.CharField(max_length=80,null=True,blank=True)
	twitter = models.CharField(max_length=80,null=True,blank=True)
	instagram = models.CharField(max_length=80,null=True,blank=True)

	def __str__(self):
		return self.user.username

