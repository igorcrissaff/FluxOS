from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
        }
