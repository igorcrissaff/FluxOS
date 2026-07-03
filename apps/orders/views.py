from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderForm

# Create your views here.
def orders_index(request):
    orders = Order.objects.all()

    pending_orders = orders.filter(status='Pending')
    completed_orders = orders.filter(status='Completed')
    cancelled_orders = orders.filter(status='Cancelled')
    shipped_orders = orders.filter(status='Shipped')
    returned_orders = orders.filter(status='Returned')

    return render(request, 'orders_index.html', {orders: orders})

def view_order(request, order_id):
    raise NotImplementedError("This view is not implemented yet")

def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(orders_index, permanent=True)
        
        else:
            return render(request, 'order_form.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'order_form.html', {'form': form})

def edit_order(request, order_id):
    raise NotImplementedError("This view is not implemented yet")

def delete_order(request, order_id):
    raise NotImplementedError("This view is not implemented yet")