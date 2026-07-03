from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.
def customers_index(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})

def view_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    raise NotImplementedError("This view is not implemented yet.")
    return render(request, 'customer_details.html', {'customer': customer})

def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(customers_index, permanent=True)
        
        else:
            return render(request, 'customer_form.html', {'form': form})
    else:
        form = CustomerForm()
        return render(request, 'customer_form.html', {'form': form})

def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect(customers_index, permanent=True)
        
        else:
            return render(request, 'customer_form.html', {'form': form})
    else:
        form = CustomerForm(instance=customer)
        return render(request, 'customer_form.html', {'form': form})

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect(customers_index, permanent=True)
