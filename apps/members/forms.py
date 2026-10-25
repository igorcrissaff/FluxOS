from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MemberForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        labels = {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'is_active': _('Active'),
            'is_staff': _('Staff'),
        }

    def __init__(self, *args, creating=False, can_manage_staff=True, **kwargs):
        self.creating = creating
        super().__init__(*args, **kwargs)

        if creating:
            self.fields['password1'].required = True
            self.fields['password2'].required = True

        if not can_manage_staff:
            self.fields.pop('is_staff', None)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', _('The two password fields did not match.'))
            elif password1:
                user = User(
                    username=cleaned_data.get('username', ''),
                    first_name=cleaned_data.get('first_name', ''),
                    last_name=cleaned_data.get('last_name', ''),
                    email=cleaned_data.get('email', ''),
                )
                try:
                    validate_password(password1, user)
                except ValidationError as error:
                    self.add_error('password1', error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user
