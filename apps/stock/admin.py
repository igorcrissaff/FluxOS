from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Movement, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('sku', 'name')
    list_display = ('id', 'sku', 'name', 'price', 'quantity', 'low_stock_threshold', 'available', 'category')
    list_filter = ('available', 'category')
    actions = ['set_available', 'set_unavailable']

    @admin.action(description=_('Set as available'))
    def set_available(self, request, queryset):
        queryset.update(available=True)
        self.message_user(request, _('Availability updated successfully.'))

    @admin.action(description=_('Set as unavailable'))
    def set_unavailable(self, request, queryset):
        queryset.update(available=False)
        self.message_user(request, _('Availability updated successfully.'))


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'reason', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__sku', 'product__name', 'reason')
    readonly_fields = ('product', 'movement_type', 'quantity', 'reason', 'created_by', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
