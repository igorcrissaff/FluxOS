from decimal import Decimal

from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from apps.customers.models import Customer
from apps.stock.models import Product


class OrderStatus(models.TextChoices):
    PENDING = 'Pending', _('Pending')
    COMPLETED = 'Completed', _('Completed')
    CANCELED = 'Canceled', _('Canceled')
    SHIPPED = 'Shipped', _('Shipped')
    RETURNED = 'Returned', _('Returned')


class Order(models.Model):
    order_number = models.CharField(_('order number'), max_length=100, unique=True)
    customer = models.ForeignKey(
        'customers.Customer',
        verbose_name=_('customer'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
    )
    order_date = models.DateTimeField(_('order date'), auto_now_add=True)
    items = models.ManyToManyField('stock.Product', verbose_name=_('items'), through='OrderItem')
    status = models.TextField(_('status'), choices=OrderStatus.choices, default=OrderStatus.PENDING)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-order_date', '-id']

    def __str__(self):
        customer = self.customer.name if self.customer else gettext('Unknown Customer')
        return gettext('Order %(number)s for %(customer)s') % {
            'number': self.order_number,
            'customer': customer,
        }

    @property
    def total(self):
        return sum((item.subtotal for item in self.orderitem_set.all()), Decimal('0.00'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    product = models.ForeignKey(
        'stock.Product',
        verbose_name=_('product'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['id']

    def __str__(self):
        product = self.product.name if self.product else gettext('Deleted Product')
        return gettext('%(quantity)s x %(product)s for Order %(order)s') % {
            'quantity': self.quantity,
            'product': product,
            'order': self.order.order_number,
        }

    @property
    def subtotal(self):
        if not self.product:
            return Decimal('0.00')
        return self.product.price * self.quantity


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'customer', 'status']
        labels = {
            'order_number': _('Order Number'),
            'customer': _('Customer'),
            'status': _('Status'),
        }


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        labels = {
            'product': _('Product'),
            'quantity': _('Quantity'),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero.'))
        return quantity
