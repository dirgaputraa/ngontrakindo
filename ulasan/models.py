# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from kontrakan.models import ProfilKontrakan
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Rating(models.Model):
	kontrakan = models.ForeignKey(ProfilKontrakan, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField()
	ulasan = models.TextField(null=True,blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	balasan = models.TextField(null=True,blank=True)
	tgl_balas = models.DateTimeField(null=True,blank=True)

	def __str__(self):
		return self.kontrakan.nama
