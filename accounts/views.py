# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def login_view(request):
	title = "Log In"
	form = UserLoginForm(request.POST or None)
	context = {
		"form": form,
		"title": title
	}
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")

	return render(request, "login.html", context)

def register_view(request):
	title = "Daftar"
	form = UserRegisterForm(request.POST or None)
	context = {
		"form": form,
		"title": title
	}
	return render(request, "regist.html", context)

def logout_view(request):
	return render(request, "login.html", {})