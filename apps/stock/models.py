from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': _('Name'),
        }


class Product(models.Model):
    sku = models.CharField(verbose_name=_('SKU'), max_length=20, unique=True)
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'), default=0)
    low_stock_threshold = models.PositiveIntegerField(verbose_name=_('Low stock threshold'), default=5)
    available = models.BooleanField(verbose_name=_('Available'), default=True)
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']

    def __str__(self):
        return f'{self.sku} - {self.name}'

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'price', 'category', 'quantity', 'low_stock_threshold', 'available']
        labels = {
            'sku': _('SKU'),
            'name': _('Name'),
            'price': _('Price'),
            'category': _('Category'),
            'quantity': _('Quantity'),
            'low_stock_threshold': _('Low stock threshold'),
            'available': _('Available'),
        }


class MovementType(models.TextChoices):
    IN = 'in', _('Stock In')
    OUT = 'out', _('Stock Out')


class Movement(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        on_delete=models.CASCADE,
        related_name='movements',
    )
    movement_type = models.CharField(_('Movement type'), max_length=10, choices=MovementType.choices)
    quantity = models.PositiveIntegerField(_('Quantity'))
    reason = models.CharField(_('Reason'), max_length=200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Created by'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Stock movement')
        verbose_name_plural = _('Stock movements')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_movement_type_display()} - {self.product} ({self.quantity})'

    @property
    def delta(self):
        return self.quantity if self.movement_type == MovementType.IN else -self.quantity

    def clean(self):
        super().clean()
        if self.quantity is not None and self.quantity <= 0:
            raise ValidationError({'quantity': _('Quantity must be greater than zero.')})
        if (
            self.product_id
            and self.quantity is not None
            and self.movement_type == MovementType.OUT
            and self.quantity > self.product.quantity
        ):
            raise ValidationError({'quantity': _('Not enough stock for this movement.')})

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError(_('Stock movements cannot be edited. Create a new movement instead.'))

        self.full_clean()

        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=self.product_id)
            new_quantity = product.quantity + self.delta
            if new_quantity < 0:
                raise ValidationError({'quantity': _('Not enough stock for this movement.')})
            product.quantity = new_quantity
            product.save(update_fields=['quantity'])
            super().save(*args, **kwargs)


class MovementForm(ModelForm):
    class Meta:
        model = Movement
        fields = ['product', 'movement_type', 'quantity', 'reason']
        labels = {
            'product': _('Product'),
            'movement_type': _('Movement type'),
            'quantity': _('Quantity'),
            'reason': _('Reason'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.order_by('name')
