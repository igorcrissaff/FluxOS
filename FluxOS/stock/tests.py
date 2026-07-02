from django.test import TestCase
from stock.models import Category, Product, Movement

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category Test')

    def test_create_category(self):
        self.assertTrue(Category.objects.exists())

    def test_str_category(self):
        self.assertEqual('Category Test', str(self.category))

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category Test')
        self.product = Product.objects.create(name='Product Test', price=10, category=self.category)

    def test_create_product(self):
        self.assertTrue(Product.objects.exists())

    def test_str_product(self):
        self.assertEqual('Product Test', str(self.product))

class MovementModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category Test')
        self.product = Product.objects.create(name='Product Test', price=10, category=self.category, quantity=0)
        self.movement = Movement.objects.create(product=self.product, quantity=10)

    def test_create_movement(self):
        self.assertTrue(Movement.objects.exists())

    def test_str_movement(self):
        self.assertEqual('Product Test - 10', str(self.movement))

    def test_update_stock_quantity_on_create(self):
        self.assertEqual(10, self.product.quantity)
    
    def test_update_stock_quantity_on_delete(self):
        self.movement.delete()
        self.assertEqual(0, self.product.quantity)

    