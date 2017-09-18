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

@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
    u = Profil.objects.filter(user=request.user)
    if u.exists():
    	us = Profil.objects.get(user=request.user)
    	us.n_login += 1
    	us.save()
    

def index(request):
	if request.user.is_authenticated():
		if request.user.first_name == '':
			return HttpResponseRedirect("/lengkapi-data/")
		else:
			queryset = Profil.objects.get(user=request.user.pk)
			if queryset.user_type == '1':
				return HttpResponseRedirect("/administrasi/")
			elif queryset.user_type == '2':
				p = Pengurus.objects.get(user=request.user)
				k = ProfilKontrakan.objects.get(id=p.kontrakan.id)
				return HttpResponseRedirect("/administrasi/dashboard/%s" % k.slug)

			context = {
				'user': queryset
			}

		return render(request, "index.html", context)

	return render(request, "index.html", {})
 		

def daftar(request):
	queryset = Profil.objects.get(user=request.user.pk)
