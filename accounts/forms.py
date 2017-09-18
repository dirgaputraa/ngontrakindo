# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("User ini tidak terdafatar.")
			if not user.check_password(password):
				raise forms.ValidationError("Password salah.")
			if not user.is_active:
				raise forms.ValidationError("User ini sudah tidak aktif.")
		
		return super(UserLoginForm, self).clean(*args, **kwargs)
		

class UserRegisterForm(forms.ModelForm):
	first_name = forms.CharField(label='Nama Depan')
	last_name = forms.CharField(label='Nama Belakang')
	email = forms.EmailField(label='Email')
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Konfirmasi Pasword', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'username',
			'email',
			'password',
			'password2'
		]

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		cek_username = User.objects.filter(username=username)
		if cek_username.exists():
			raise forms.ValidationError("Username ini sudah digunakan")
		email = self.cleaned_data.get('email')
		cek_email = User.objects.filter(email=email)
		if cek_email.exists():
			raise forms.ValidationError("Email ini sudah terdaftar")
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Konfirmasi password tidak cocok")

		return super(UserRegisterForm, self).clean(*args, **kwargs)