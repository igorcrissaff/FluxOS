from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(verbose_name='nome', max_length=100)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(verbose_name='nome', max_length=100)
    price = models.DecimalField(verbose_name='preço', max_digits=5, decimal_places=2)
    quantity = models.IntegerField(verbose_name='quantidade', default=0)
    category = models.ForeignKey(Category, verbose_name='categoria', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'quantity': self.quantity,
            'Category': self.Category.name
        }
    
class Movement(models.Model):
    product = models.ForeignKey(Product, verbose_name='produto', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='quantidade')
    date = models.DateTimeField(verbose_name='data', auto_now_add=True)

    class Meta:
        verbose_name = _('Movimentação')
        verbose_name_plural = _('Movimentações')

    def __str__(self):
        return f"{self.Product} - {self.quantity}"
