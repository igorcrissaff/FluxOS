from django.contrib import admin
from .models import Category, Product, Movement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('id__startswith', 'name__startswith')
    list_display = ('id', 'name', 'price', 'quantity', 'category')
    list_filter = ('category', )

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    pass
