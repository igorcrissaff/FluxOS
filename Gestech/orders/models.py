from django.db import models

# Create your models here.
class Customer(models.Model):
    # Personal information fields
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    # Address fields
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)

    @property
    def address(self):
        return f"{self.street}, {self.house_number} - {self.city} - {self.state}"

    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    content = models.ManyToManyField('stock.Product', through='OrderItem')
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.order_number