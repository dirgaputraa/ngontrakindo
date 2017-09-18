# -*- coding: utf-8 -*-

from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):

        data = form.cleaned_data
        # user.first_name = data['first_name']
        # user.last_name = data['last_name']
        user.username = data['username']
        user.email = data['email']
        user.password = data['password1']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user