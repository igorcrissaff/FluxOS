from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
    MALE = 'Male', _('Male')
    FEMALE = 'Female', _('Female')
    OTHER = 'Other', _('Other')

class MaritalStatusChoices(models.TextChoices):
    SINGLE = 'Single', _('Single')
    MARRIED = 'Married', _('Married')
    DIVORCED = 'Divorced', _('Divorced')
    WIDOWED = 'Widowed', _('Widowed')

class Customer(models.Model):
    # Contact Info
    name = models.CharField(_('name'), max_length=100)
    phone = models.CharField(_('phone'), max_length=15)

    # Shipping Address
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    state = models.CharField(_('state'), max_length=100, blank=True, null=True)
    street = models.CharField(_('street'), max_length=200, blank=True, null=True)
    house_number = models.CharField(_('house number'), max_length=10, blank=True, null=True)

    # Statistic Fields
    total_orders = models.IntegerField(_('total orders'), default=0)
    total_spent = models.DecimalField(_('total spent'), max_digits=10, decimal_places=2, default=0)
    gender = models.TextField(_('gender'), choices=GenderChoices.choices, default=GenderChoices.OTHER)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    marital_status = models.CharField(_('marital status'), max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['name']

    @property
    def address(self):
        parts = [
            ', '.join(part for part in [self.street, self.house_number] if part),
            ' / '.join(part for part in [self.city, self.state] if part),
        ]
        return ' - '.join(part for part in parts if part) or '-'

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'gender',
            'marital_status',
            'birthday',
            'city',
            'state',
            'street',
            'house_number',
        ]
        labels = {
            'name': _('Name'),
            'phone': _('Phone'),
            'gender': _('Gender'),
            'marital_status': _('Marital Status'),
            'birthday': _('Birthday'),
            'city': _('City'),
            'state': _('State'),
            'street': _('Street'),
            'house_number': _('House Number'),
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }