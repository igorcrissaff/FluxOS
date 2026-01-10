from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(verbose_name='nome', max_length=100)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
    
    def __str__(self):
        return self.name  

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': _('Nome'),
        }

class Product(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    sku = models.CharField(verbose_name='sku', max_length=20, unique=True)  
    name = models.CharField(verbose_name='nome', max_length=100)
    price = models.DecimalField(verbose_name='preço', max_digits=5, decimal_places=2)
    quantity = models.IntegerField(verbose_name='quantidade', default=0)
    category = models.ForeignKey(Category, verbose_name='categoria', on_delete=models.SET_NULL, null=True)
    avaliable = models.BooleanField(verbose_name='disponível', default=True)

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    def __str__(self):
        return f"{self.name}"
    
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

    # Definir disponibilidade
    def set_avaliability(self, avaliable):
        self.avaliable = avaliable
        self.save()
    
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'price', 'quantity', 'category', 'avaliable']
        labels = {
            'sku': _('SKU'),
            'name': _('Nome'),
            'price': _('Preço'),
            'quantity': _('Quantidade'),
            'category': _('Categoria'),
            'avaliable': _('Disponível'),
        }