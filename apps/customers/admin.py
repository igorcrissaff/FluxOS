from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'state', 'total_orders', 'total_spent')
    search_fields = ('name', 'phone', 'city', 'state')
    list_filter = ('gender', 'state')
    readonly_fields = ('total_orders', 'total_spent')
