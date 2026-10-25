from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import Order, OrderForm, OrderItem, OrderItemForm, OrderStatus
from .services import update_customer_stats

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


@login_required
def orders_index(request):
    orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product')
    status = request.GET.get('status')
    status_label = None

    if status in OrderStatus.values:
        orders = orders.filter(status=status)
        status_label = dict(OrderStatus.choices).get(status)
    else:
        status = ''

    return render(
        request,
        'orders_index.html',
        {
            'orders': orders,
            'status': status,
            'status_label': status_label,
        },
    )


@login_required
def view_order(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('customer').prefetch_related('orderitem_set__product'),
        id=order_id,
    )
    return render(request, 'order_details.html', {'order': order})


@login_required
def create_order(request):
    order = Order()

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save()
                formset.instance = order
                formset.save()
                update_customer_stats(order.customer)
            messages.success(request, _('Order created successfully.'))
            return redirect('view_order', order_id=order.id)
    else:
        initial = {}
        customer_id = request.GET.get('customer')
        if customer_id:
            initial['customer'] = customer_id
        form = OrderForm(instance=order, initial=initial)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'order_form.html', {'form': form, 'formset': formset})


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    old_customer = order.customer

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save()
                formset.save()
                update_customer_stats(old_customer)
                update_customer_stats(order.customer)
            messages.success(request, _('Order updated successfully.'))
            return redirect('view_order', order_id=order.id)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'order_form.html', {'form': form, 'formset': formset, 'order': order})


@login_required
@require_POST
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    order.delete()
    update_customer_stats(customer)
    messages.success(request, _('Order deleted successfully.'))
    return redirect('orders_index')
