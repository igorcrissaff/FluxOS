from django.contrib import admin

from apps.customers.models import Customer

from .models import Order, OrderItem
from .services import update_customer_stats


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__name')
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        self._old_customer = Order.objects.get(pk=obj.pk).customer if change else None
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        update_customer_stats(getattr(self, '_old_customer', None))
        update_customer_stats(form.instance.customer)

    def delete_model(self, request, obj):
        customer = obj.customer
        super().delete_model(request, obj)
        update_customer_stats(customer)

    def delete_queryset(self, request, queryset):
        customers = list(queryset.exclude(customer=None).values_list('customer', flat=True).distinct())
        super().delete_queryset(request, queryset)
        for customer in customers:
            update_customer_stats(Customer.objects.filter(pk=customer).first())


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_number', 'product__name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_customer_stats(obj.order.customer)

    def delete_model(self, request, obj):
        customer = obj.order.customer
        super().delete_model(request, obj)
        update_customer_stats(customer)

    def delete_queryset(self, request, queryset):
        customers = list(
            queryset.exclude(order__customer=None)
            .values_list('order__customer', flat=True)
            .distinct()
        )
        super().delete_queryset(request, queryset)
        for customer in customers:
            update_customer_stats(Customer.objects.filter(pk=customer).first())
