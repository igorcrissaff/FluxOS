from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import Customer, CustomerForm


@login_required
def customers_index(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})


@login_required
def view_customer(request, customer_id):
    customer = get_object_or_404(
        Customer.objects.prefetch_related('orders__orderitem_set__product'),
        id=customer_id,
    )
    return render(request, 'customer_details.html', {'customer': customer})


@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Customer created successfully.'))
            return redirect('customers_index')
    else:
        form = CustomerForm()

    return render(request, 'customer_form.html', {'form': form})


@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, _('Customer updated successfully.'))
            return redirect('view_customer', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_form.html', {'form': form, 'customer': customer})


@login_required
@require_POST
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    messages.success(request, _('Customer deleted successfully.'))
    return redirect('customers_index')
