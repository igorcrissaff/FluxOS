from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.customers.models import Customer
from apps.orders.models import Order, OrderStatus
from apps.stock.models import Product

from .forms import ProfileForm


@login_required
def dashboard(request):
    today = timezone.localdate()
    revenue_statuses = [OrderStatus.COMPLETED, OrderStatus.SHIPPED]
    orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product')

    monthly_orders = orders.filter(
        status__in=revenue_statuses,
        order_date__year=today.year,
        order_date__month=today.month,
    )
    annual_orders = orders.filter(status__in=revenue_statuses, order_date__year=today.year)

    monthly_revenue = sum((order.total for order in monthly_orders), Decimal('0.00'))
    annual_revenue = sum((order.total for order in annual_orders), Decimal('0.00'))
    pending_orders_count = orders.filter(status=OrderStatus.PENDING).count()
    low_stock_products = Product.objects.filter(
        available=True,
        quantity__lte=F('low_stock_threshold'),
    ).order_by('quantity', 'name')

    return render(
        request,
        'dashboard.html',
        {
            'monthly_revenue': monthly_revenue,
            'annual_revenue': annual_revenue,
            'pending_orders_count': pending_orders_count,
            'low_stock_products': low_stock_products,
            'low_stock_count': low_stock_products.count(),
            'recent_orders': orders.order_by('-order_date')[:5],
            'top_customers': Customer.objects.order_by('-total_spent')[:5],
        },
    )


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully.'))
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})
