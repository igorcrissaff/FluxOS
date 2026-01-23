from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(verbose_name='nome', max_length=100)
    ascending = models.ForeignKey('self', verbose_name='categoria ascendente', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
    
    def __str__(self):
        return self.name  

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'ascending']
        labels = {
            'name': _('Nome'),
            'ascending': _('Categoria Ascendente'),
        }
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Product(models.Model):
    sku = models.CharField(verbose_name='sku', max_length=20, unique=True)  
    name = models.CharField(verbose_name='nome', max_length=100)
    price = models.DecimalField(verbose_name='preço', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name='quantidade', default=0)
    category = models.ForeignKey(Category, verbose_name='categoria', on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    def __str__(self):
        return f"{self.sku} - {self.name}"
    
    def json(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "price": float(self.price),
            "quantity": self.quantity,
            "category": self.category.name if self.category else None,
            "avaliable": self.avaliable,
        }
    
    # Mudar estoque
    def change_quantity(self, quantity):
        self.quantity += quantity
        InventoryLog.objects.create(
            product=self.id,
            change_type='Ajuste de Estoque',
            quantity_changed=quantity
        )
        self.save()

    # Corrigir estoque
    def correct_quantity(self, quantity):
        self.quantity = quantity
        self.save()

    # Aplicar desconto direto
    def apply_direct_discount(self, discount):
        self.price -= discount
        self.save()

    # Aplicar desconto percentual
    def apply_percentage_discount(self, percentage):
        self.price -= (self.price * percentage / 100)
        self.save()
    
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'price', 'category', 'quantity']
        labels = {
            'sku': _('SKU'),
            'name': _('Nome'),
            'price': _('Preço'),
            'category': _('Categoria'),
            'quantity': _('Quantidade'),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

