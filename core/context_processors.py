from django.db.models import F


def alerts(request):
    if not request.user.is_authenticated:
        return {}

    from apps.orders.models import Order, OrderStatus
    from apps.stock.models import Product

    low_stock = Product.objects.filter(
        available=True,
        quantity__lte=F('low_stock_threshold'),
    ).order_by('quantity', 'name')

    pending_orders = Order.objects.filter(status=OrderStatus.PENDING).count()
    low_stock_count = low_stock.count()

    return {
        'low_stock_alerts': low_stock[:5],
        'low_stock_count': low_stock_count,
        'pending_order_alerts': pending_orders,
        'alert_count': low_stock_count + pending_orders,
    }
