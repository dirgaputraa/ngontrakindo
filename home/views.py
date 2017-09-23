# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from profiles.models import Profil
from kontrakan.models import *
from django.dispatch.dispatcher import receiver
from allauth.account.signals import user_logged_in
from profiles.models import *

def index(request):
	if request.user.is_authenticated():
		if request.user.first_name == '':
			return HttpResponseRedirect("/lengkapi-data/")
		else:
			queryset, created = Profil.objects.get_or_create(user=request.user, defaults={'user_type': '3'})
			if queryset.user_type == '1':
				kon = ProfilKontrakan.objects.get()
				return HttpResponseRedirect("/administrasi/dashboard/%s" % kon.slug)
			elif queryset.user_type == '2':
				p = Pengurus.objects.get(user=request.user)
				k = ProfilKontrakan.objects.get(id=p.kontrakan.id)
				return HttpResponseRedirect("/administrasi/dashboard/%s" % k.slug)

			context = {
				'user': queryset
			}

		return render(request, "index.html", context)

	return HttpResponseRedirect("/accounts/login")
 		

def daftar(request):
	queryset = Profil.objects.get(user=request.user.pk)
