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
    

