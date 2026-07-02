from django.db import models
from django.forms import ModelForm

class GenderChoices(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHER = 'Other', 'Other'

class MaritalStatusChoices(models.TextChoices):
    SINGLE = 'Single', 'Single'
    MARRIED = 'Married', 'Married'
    DIVORCED = 'Divorced', 'Divorced'
    WIDOWED = 'Widowed', 'Widowed'

class Customer(models.Model):
    # Contact Info
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    # Shipping Address
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)

    # Statistic Fields
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gender = models.TextField(choices=GenderChoices.choices, default=GenderChoices.OTHER)
    birthday = models.DateField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)

    @property
    def address(self):
        return f"{self.street}, {self.house_number} - {self.city} / {self.state}"

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'gender', 'marital_status', 'city', 'state', 'street', 'house_number']