from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Category, Movement, MovementType, Product


class CategoryModelTest(TestCase):
    def test_str_category(self):
        category = Category.objects.create(name='Category Test')
        self.assertEqual(str(category), 'Category Test')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category Test')

    def test_str_product_includes_sku(self):
        product = Product.objects.create(
            sku='SKU-1',
            name='Product Test',
            price=Decimal('10.00'),
            category=self.category,
        )
        self.assertEqual(str(product), 'SKU-1 - Product Test')

    def test_is_low_stock_at_threshold(self):
        product = Product.objects.create(
            sku='SKU-1',
            name='Product Test',
            price=Decimal('10.00'),
            quantity=5,
            low_stock_threshold=5,
        )
        self.assertTrue(product.is_low_stock)

    def test_is_not_low_stock_above_threshold(self):
        product = Product.objects.create(
            sku='SKU-1',
            name='Product Test',
            price=Decimal('10.00'),
            quantity=6,
            low_stock_threshold=5,
        )
        self.assertFalse(product.is_low_stock)


class MovementModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            sku='SKU-1',
            name='Product Test',
            price=Decimal('10.00'),
            quantity=10,
        )

    def test_stock_in_increments_product_quantity(self):
        Movement.objects.create(
            product=self.product,
            movement_type=MovementType.IN,
            quantity=4,
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 14)

    def test_stock_out_decrements_product_quantity(self):
        Movement.objects.create(
            product=self.product,
            movement_type=MovementType.OUT,
            quantity=4,
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 6)

    def test_stock_out_above_available_quantity_is_rejected(self):
        with self.assertRaises(ValidationError):
            Movement.objects.create(
                product=self.product,
                movement_type=MovementType.OUT,
                quantity=11,
            )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValidationError):
            Movement.objects.create(
                product=self.product,
                movement_type=MovementType.IN,
                quantity=0,
            )

    def test_existing_movement_cannot_be_edited(self):
        movement = Movement.objects.create(
            product=self.product,
            movement_type=MovementType.IN,
            quantity=1,
        )
        movement.quantity = 2
        with self.assertRaises(ValidationError):
            movement.save()

    def test_delta_for_in_and_out_movements(self):
        stock_in = Movement.objects.create(
            product=self.product,
            movement_type=MovementType.IN,
            quantity=3,
        )
        stock_out = Movement.objects.create(
            product=self.product,
            movement_type=MovementType.OUT,
            quantity=2,
        )

        self.assertEqual(stock_in.delta, 3)
        self.assertEqual(stock_out.delta, -2)

    def test_string_representation(self):
        movement = Movement.objects.create(
            product=self.product,
            movement_type=MovementType.IN,
            quantity=3,
        )

        self.assertIn('Stock In', str(movement))
        self.assertIn('SKU-1', str(movement))
        self.assertIn('3', str(movement))


class StockViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='staff',
            password='testpass123',
            is_staff=True,
        )
        cls.category = Category.objects.create(name='Category Test')
        cls.product = Product.objects.create(
            sku='SKU-1',
            name='Product Test',
            price=Decimal('10.00'),
            quantity=1,
            low_stock_threshold=5,
            category=cls.category,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_stock_pages_require_login(self):
        self.client.logout()
        response = self.client.get(reverse('stock_index'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('stock_index')}")

    def test_low_stock_filter(self):
        Product.objects.create(
            sku='SKU-2',
            name='Healthy Product',
            price=Decimal('10.00'),
            quantity=10,
            low_stock_threshold=5,
        )
        response = self.client.get(reverse('stock_index'), {'low_stock': '1'})
        products = list(response.context['products'])
        self.assertEqual(products, [self.product])
        self.assertEqual(response.context['low_stock_products'].count(), 1)

    def test_create_product(self):
        response = self.client.post(
            reverse('create_product'),
            {
                'sku': 'SKU-NEW',
                'name': 'New Product',
                'price': '12.50',
                'category': self.category.pk,
                'quantity': '3',
                'low_stock_threshold': '2',
                'available': 'on',
            },
        )
        self.assertRedirects(response, reverse('stock_index'))
        product = Product.objects.get(sku='SKU-NEW')
        self.assertEqual(product.quantity, 3)
        self.assertTrue(product.available)

    def test_delete_product_requires_post(self):
        response = self.client.get(reverse('delete_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        response = self.client.post(reverse('delete_product', args=[self.product.pk]))
        self.assertRedirects(response, reverse('stock_index'))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_create_stock_movement(self):
        response = self.client.post(
            reverse('create_movement'),
            {
                'product': self.product.pk,
                'movement_type': MovementType.IN,
                'quantity': '4',
                'reason': 'Restock',
            },
        )
        self.assertRedirects(response, reverse('movements'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)
        movement = Movement.objects.get(product=self.product)
        self.assertEqual(movement.created_by, self.user)

    def test_insufficient_stock_movement_shows_error(self):
        response = self.client.post(
            reverse('create_movement'),
            {
                'product': self.product.pk,
                'movement_type': MovementType.OUT,
                'quantity': '2',
                'reason': 'Sale',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Not enough stock for this movement.')
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 1)

    def test_all_stock_pages_require_login(self):
        self.client.logout()
        urls = [
            reverse('stock_index'),
            reverse('create_product'),
            reverse('edit_product', args=[self.product.pk]),
            reverse('categories'),
            reverse('edit_category', args=[self.category.pk]),
            reverse('movements'),
            reverse('create_movement'),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_edit_product(self):
        response = self.client.post(
            reverse('edit_product', args=[self.product.pk]),
            {
                'sku': 'SKU-EDITED',
                'name': 'Edited Product',
                'price': '15.00',
                'category': '',
                'quantity': '7',
                'low_stock_threshold': '3',
                'available': 'on',
            },
        )

        self.assertRedirects(response, reverse('stock_index'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.sku, 'SKU-EDITED')
        self.assertEqual(self.product.name, 'Edited Product')
        self.assertEqual(self.product.price, Decimal('15.00'))
        self.assertEqual(self.product.quantity, 7)
        self.assertTrue(self.product.available)
        self.assertIsNone(self.product.category)

    def test_create_product_rejects_duplicate_sku(self):
        response = self.client.post(
            reverse('create_product'),
            {
                'sku': self.product.sku,
                'name': 'Duplicate SKU',
                'price': '10.00',
                'category': self.category.pk,
                'quantity': '1',
                'low_stock_threshold': '5',
                'available': 'on',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('sku', response.context['form'].errors)
        self.assertEqual(Product.objects.count(), 1)

    def test_missing_product_returns_404(self):
        response = self.client.get(reverse('edit_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('delete_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_edit_and_delete_category(self):
        response = self.client.post(reverse('categories'), {'name': 'New Category'})
        self.assertRedirects(response, reverse('categories'))
        category = Category.objects.get(name='New Category')

        response = self.client.post(
            reverse('edit_category', args=[category.pk]),
            {'name': 'Updated Category'},
        )
        self.assertRedirects(response, reverse('categories'))
        category.refresh_from_db()
        self.assertEqual(category.name, 'Updated Category')

        response = self.client.post(reverse('delete_category', args=[category.pk]))
        self.assertRedirects(response, reverse('categories'))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

    def test_delete_category_requires_post(self):
        response = self.client.get(reverse('delete_category', args=[self.category.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())

    def test_deleting_category_detaches_products(self):
        response = self.client.post(reverse('delete_category', args=[self.category.pk]))

        self.assertRedirects(response, reverse('categories'))
        self.product.refresh_from_db()
        self.assertIsNone(self.product.category)

    def test_low_stock_filter_excludes_unavailable_products(self):
        Product.objects.create(
            sku='SKU-UNAVAILABLE',
            name='Unavailable Low Stock',
            price=Decimal('10.00'),
            quantity=0,
            low_stock_threshold=5,
            available=False,
        )

        response = self.client.get(reverse('stock_index'), {'low_stock': '1'})

        products = list(response.context['products'])
        self.assertEqual(products, [self.product])
        self.assertEqual(response.context['low_stock_products'].count(), 1)

    def test_stock_summary_metrics(self):
        Product.objects.create(
            sku='SKU-HEALTHY',
            name='Healthy Product',
            price=Decimal('2.00'),
            quantity=10,
            low_stock_threshold=5,
            available=True,
        )
        Product.objects.create(
            sku='SKU-OUT',
            name='Out of Stock Product',
            price=Decimal('99.00'),
            quantity=0,
            low_stock_threshold=5,
            available=False,
        )

        response = self.client.get(reverse('stock_index'))

        self.assertEqual(response.context['stock_value'], Decimal('30.00'))
        self.assertEqual(response.context['total_stock'], 11)
        self.assertEqual(response.context['low_stock_products'].count(), 1)
        self.assertEqual(response.context['products_out_of_stock'].count(), 1)
        self.assertEqual(response.context['active_products'].count(), 2)

    def test_create_movement_prefills_selected_product(self):
        response = self.client.get(
            reverse('create_movement'),
            {'product': self.product.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.context['form'].initial['product']),
            str(self.product.pk),
        )

    def test_stock_out_movement_decrements_quantity(self):
        response = self.client.post(
            reverse('create_movement'),
            {
                'product': self.product.pk,
                'movement_type': MovementType.OUT,
                'quantity': '1',
                'reason': 'Sale',
            },
        )

        self.assertRedirects(response, reverse('movements'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 0)
        self.assertEqual(Movement.objects.get().created_by, self.user)

    def test_movements_index_lists_history(self):
        Movement.objects.create(
            product=self.product,
            movement_type=MovementType.IN,
            quantity=4,
            reason='Restock',
        )

        response = self.client.get(reverse('movements'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restock')
        self.assertContains(response, self.product.sku)
