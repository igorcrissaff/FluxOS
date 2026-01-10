from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('id__startswith', 'name__startswith')
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'avaliable')
    list_filter = ('category',)
    actions = ['set_avaliable', 'set_unavaliabe']

    @admin.action(description='Definir como Disponivel')
    def set_avaliable(self, request, queryset):
        queryset.update(avaliable=True)
        self.message_user(request, "Disponibilidade definida com sucesso.")

    @admin.action(description='Definir como Indisponivel')
    def set_unavaliabe(self, request, queryset):
        queryset.update(avaliable=False)
        self.message_user(request, "Disponibilidade definida com sucesso.")

"""@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    readonly_fields = ('product', 'quantity', 'date')
    list_display = ('product', 'quantity', 'date')"""
