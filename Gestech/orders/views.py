from django.shortcuts import render
from .models import Order

# Create your views here.
def orders_index(request):
    orders = Order.objects.all()

    pending_orders = orders.filter(status='Pending')
    completed_orders = orders.filter(status='Completed')
    cancelled_orders = orders.filter(status='Cancelled')
    shipped_orders = orders.filter(status='Shipped')
    returned_orders = orders.filter(status='Returned')

    raise NotImplementedError("This view is not implemented yet")

def view_order(request, order_id):
    raise NotImplementedError("This view is not implemented yet")

def create_order(request):
    raise NotImplementedError("This view is not implemented yet")

def edit_order(request, order_id):
    raise NotImplementedError("This view is not implemented yet")

def delete_order(request, order_id):
    raise NotImplementedError("This view is not implemented yet")