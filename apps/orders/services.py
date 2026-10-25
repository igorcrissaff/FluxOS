from decimal import Decimal

from .models import OrderStatus


def update_customer_stats(customer):
    if customer is None:
        return

    active_orders = customer.orders.exclude(status__in=[OrderStatus.CANCELED, OrderStatus.RETURNED])
    revenue_orders = customer.orders.filter(status__in=[OrderStatus.COMPLETED, OrderStatus.SHIPPED])
    total_spent = sum((order.total for order in revenue_orders), Decimal('0.00'))

    customer.total_orders = active_orders.count()
    customer.total_spent = total_spent
    customer.save(update_fields=['total_orders', 'total_spent'])
