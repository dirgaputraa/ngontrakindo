# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import Nama, ProfilForm, AvatarForm, UserForm
from .models import Profil, Medsos
from django.shortcuts import get_object_or_404
from django.core.files.images import get_image_dimensions
from PIL import Image
from kontrakan.models import (
	ProfilKontrakan,
	Penghuni,
	FotoKontrakan,
	Pengurus,
)
import datetime

User = get_user_model()

@login_required(login_url='/accounts/login/')
def lengkapi(request):
	form = Nama(request.POST or None)
	if form.is_valid():
		if request.user.is_authenticated():
			user = form.save(commit=False)
			f = form.cleaned_data.get("first_name")
			g = form.cleaned_data.get("last_name")
			u = request.user.username
			get = User.objects.get(username=u)
			get.first_name = f
			get.last_name = g
			get.save()
			return HttpResponseRedirect("/lengkapi-data-2/")
		else:
			return HttpResponseRedirect("/accounts/login/")

	context = {
		"form": form
	}
	return render(request, "account/nama.html", context)

@login_required(login_url='/accounts/login/')
def lengkapi2(request):
	form = ProfilForm(request.POST or None)
	if form.is_valid():
		if request.user.is_authenticated():
			profil = form.save(commit=False)
			tgl_lahir = form.cleaned_data.get("tgl_lahir")
			jk = form.cleaned_data.get("jk")
			alamat = form.cleaned_data.get("alamat")
			no_telp = form.cleaned_data.get("no_telp")
			profesi = form.cleaned_data.get("profesi")
			instansi = form.cleaned_data.get("instansi")
			profil.user = request.user
			profil.tgl_lahir = tgl_lahir
			profil.jk = jk
			profil.alamat = alamat
			profil.no_telp = no_telp
			profil.profesi = profesi
			profil.instansi = instansi
			profil.save()
			return HttpResponseRedirect("/%s" % request.user.username)
		else:
			return HttpResponseRedirect("/accounts/login/")

	context = {
		"form": form
	}
	return render(request, "account/detail.html", context)

def profil_detail(request, username):
	x = get_object_or_404(User, username=username)
	today = datetime.datetime.now()
	if request.user.username != username:
		queryset = get_object_or_404(Profil, user=x)
		p = Penghuni.objects.filter(user=x)
	else:
		queryset = get_object_or_404(Profil, user=request.user.pk)
		p = Penghuni.objects.filter(user=request.user)

	if queryset.user_type == '1':
		kont = ProfilKontrakan.objects.filter(pemilik=x)
		f = []
		wr = []
		for k in kont:
			if k.kategori == '1':
				wn = 'w3-green'
			elif k.kategori == '2':
				wn = 'w3-indigo'
			elif k.kategori == '3':
				wn = 'w3-brown'
			elif k.kategori == '4':
				wn = 'w3-pink'
			elif k.kategori == '5':
				wn = 'w3-purple'
			wr.append(wn)
			m = FotoKontrakan.objects.filter(kontrakan=k,foto_utama=True)
			if m.exists():
				f.append(m[0].foto.url)
			else:
				f.append('/media/logo3.png')

		z_kont = zip(kont,f,wr)
	elif queryset.user_type == '2':
		pngr = Pengurus.objects.get(user=x)
		kont = ProfilKontrakan.objects.get(id=pngr.kontrakan.id)
		z_kont = ''
	else:
		kont = ''
		z_kont = ''
	
	if p.exists():
		ktr = []
		ft = []
		w = []
		status = []
		for pp in p:
			if pp.aktif and pp.konfirm:
				s = 'Penghuni'
			elif not pp.aktif and pp.konfirm:
				s = 'Eks Penghuni'
			else:
				s = 'Pending'

			status.append(s)
			a = ProfilKontrakan.objects.get(nama=pp.kontrakan)
			if a.kategori == '1':
				warna = 'w3-green'
			elif a.kategori == '2':
				warna = 'w3-indigo'
			elif a.kategori == '3':
				warna = 'w3-brown'
			elif a.kategori == '4':
				warna = 'w3-pink'
			elif a.kategori == '5':
				warna = 'w3-purple'
			ktr.append(a)
			w.append(warna)
			ft.append(FotoKontrakan.objects.get(kontrakan=pp.kontrakan,foto_utama=True))
		z_png = zip(ktr,ft,status,w)
	else:
		z_png = ""

	m = Medsos.objects.filter(user=x)
	if m.exists():
		fb = m[0].facebook
		tw = m[0].twitter
		ins = m[0].instagram
	else:
		fb = ''
		tw = ''
		ins = ''

	context = {
		"user": queryset,
		"x": x,
		"kontrakan": kont,
		"p": p,
		"fb": fb,
		"tw": tw,
		"ins": ins,
		"z_kont": z_kont,
		"z_png": z_png,
	}

	return render(request, "profile.html", context)

@login_required(login_url='/accounts/login/')
def avatar_edit(request):
	queryset = get_object_or_404(Profil, user=request.user.pk)
	user = Profil.objects.filter(user=request.user.pk)
	u = User.objects.get(username=queryset.user)
	form = AvatarForm(request.POST, request.FILES)

	m = Medsos.objects.filter(user=u)
	if m.exists():
		fb = m[0].facebook
		tw = m[0].twitter
		ins = m[0].instagram
	else:
		fb = ''
		tw = ''
		ins = ''

	if request.method == 'POST':
		if form.is_valid():
			img = form.save(commit=False)
			x = form.cleaned_data.get('x')
	        y = form.cleaned_data.get('y')
	        w = form.cleaned_data.get('width')
	        h = form.cleaned_data.get('height')
	        print(img.avatar)

	        image = Image.open(img.avatar)
	        cropped_image = image.crop((x, y, w+x, h+y))
	        resized_image = cropped_image.resize((180, 180), Image.ANTIALIAS)
	        resized_image.save(img.avatar.path)
	        user.update(avatar=img.avatar)
	        return HttpResponseRedirect("/%s" % request.user.username)

	else:
		form = AvatarForm()

	form2 = ProfilForm(request.POST or None,
		initial={
		'tgl_lahir': queryset.tgl_lahir,
		'jk': queryset.jk,
		'alamat': queryset.alamat,
		'no_telp': queryset.no_telp,
		'profesi': queryset.profesi,
		'instansi': queryset.instansi
		})
	form3 = UserForm(request.POST or None,
		initial={
		'first_name': u.first_name,
		'last_name': u.last_name,
		'username': u.username,
		})

	context = {
		'user': queryset,
		'x': u,
		'form': form,
		"fb": fb,
		"tw": tw,
		"ins": ins,
		'form2': form2,
		'form3': form3
	}

	return render(request, "editprofil.html", context)

@login_required(login_url='/accounts/login/')
def profil_edit(request):
	user = Profil.objects.filter(user=request.user.pk)
	uname = request.user.username
	form2 = ProfilForm(request.POST or None)
	if form2.is_valid():
		frm2 = form2.save(commit=False)
		tgl_lahir = form2.cleaned_data.get('tgl_lahir')
		jk = form2.cleaned_data.get('jk')
		alamat = form2.cleaned_data.get('alamat')
		no_telp = form2.cleaned_data.get('no_telp')
		profesi = form2.cleaned_data.get('profesi')
		instansi = form2.cleaned_data.get('instansi')
		user.update(
			tgl_lahir=tgl_lahir,
			jk=jk,
			alamat=alamat,
			no_telp=no_telp,
			profesi=profesi,
			instansi=instansi
		)
		return HttpResponseRedirect("/%s" % uname)

	return redirect('editprofil')

@login_required(login_url='/accounts/login/')
def akun_edit(request):
	uname = request.user.username
	if request.method == 'POST':
		form3 = UserForm(data=request.POST, instance=request.user)
		if form3.is_valid():
			frm2 = form3.save(commit=False)
			frm2.save()
			return HttpResponseRedirect("/%s" % form3.cleaned_data.get('username'))

	return redirect('editprofil')

@login_required(login_url='/accounts/login/')
def medsos_edit(request):
	if request.method == 'POST':
		u = request.user
		f = request.POST['facebook']
		t = request.POST['twitter']
		i = request.POST['instagram']
		Medsos.objects.update_or_create(user=u,defaults={'facebook': f,'twitter': t,'instagram': i})

	return redirect('editprofil')
		

# def photo_list(request):
#     photos = Profil.objects.all()
#     if request.method == 'POST':
#         form = PhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('photo_list')
#     else:
#         form = PhotoForm()
#     return render(request, 'album/photo_list.html', {'form': form, 'photos': photos})