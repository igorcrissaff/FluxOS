from django.db import models
from django.forms import ModelForm
from apps.customers.models import Customer
from apps.stock.models import Product

class OrderStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    CANCELED = 'Canceled', 'Canceled'
    SHIPPED = 'Shipped', 'Shipped'
    RETURNED = 'Returned', 'Returned'

class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('stock.Product', through='OrderItem')
    status = models.TextField(choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Order {self.order_number} for {self.customer.name if self.customer else 'Unknown Customer'}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('stock.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.order_number}"
    
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'customer', 'items', 'status']