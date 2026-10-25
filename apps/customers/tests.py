from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.orders.models import Order, OrderItem, OrderStatus
from apps.stock.models import Product

from .models import Customer, CustomerForm


class CustomerModelTest(TestCase):
    def test_address_formats_available_parts(self):
        customer = Customer.objects.create(
            name='Customer',
            phone='123',
            street='Main Street',
            house_number='10',
            city='Sao Paulo',
            state='SP',
        )
        self.assertEqual(customer.address, 'Main Street, 10 - Sao Paulo / SP')

    def test_address_defaults_to_dash(self):
        customer = Customer.objects.create(name='Customer', phone='123')
        self.assertEqual(customer.address, '-')

    def test_address_with_street_only(self):
        customer = Customer.objects.create(
            name='Customer',
            phone='123',
            street='Main Street',
        )
        self.assertEqual(customer.address, 'Main Street')

    def test_address_with_city_and_state_only(self):
        customer = Customer.objects.create(
            name='Customer',
            phone='123',
            city='Sao Paulo',
            state='SP',
        )
        self.assertEqual(customer.address, 'Sao Paulo / SP')


class CustomerFormTest(TestCase):
    def test_statistic_fields_are_not_exposed(self):
        form = CustomerForm()

        self.assertNotIn('total_orders', form.fields)
        self.assertNotIn('total_spent', form.fields)


class CustomerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='staff',
            password='testpass123',
            is_staff=True,
        )
        cls.customer = Customer.objects.create(name='Customer', phone='123')

    def setUp(self):
        self.client.force_login(self.user)

    def test_customer_pages_require_login(self):
        self.client.logout()
        response = self.client.get(reverse('customers_index'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('customers_index')}")

    def test_customer_details_show_order_history(self):
        product = Product.objects.create(
            sku='SKU-1',
            name='Product',
            price=Decimal('10.00'),
            quantity=10,
        )
        order = Order.objects.create(
            order_number='ORD-1',
            customer=self.customer,
            status=OrderStatus.COMPLETED,
        )
        OrderItem.objects.create(order=order, product=product, quantity=2)

        response = self.client.get(reverse('view_customer', args=[self.customer.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORD-1')
        self.assertContains(response, 'Product')
        self.assertEqual(list(response.context['customer'].orders.all()), [order])

    def test_create_customer(self):
        response = self.client.post(
            reverse('create_customer'),
            {
                'name': 'New Customer',
                'phone': '999',
                'gender': 'Other',
                'marital_status': '',
                'birthday': '',
                'city': '',
                'state': '',
                'street': '',
                'house_number': '',
            },
        )
        self.assertRedirects(response, reverse('customers_index'))
        customer = Customer.objects.get(name='New Customer')
        self.assertEqual(customer.phone, '999')

    def test_edit_customer(self):
        response = self.client.post(
            reverse('edit_customer', args=[self.customer.pk]),
            {
                'name': 'Updated Customer',
                'phone': '456',
                'gender': 'Other',
                'marital_status': '',
                'birthday': '',
                'city': '',
                'state': '',
                'street': '',
                'house_number': '',
            },
        )
        self.assertRedirects(response, reverse('view_customer', args=[self.customer.pk]))
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Updated Customer')

    def test_delete_customer_requires_post(self):
        response = self.client.get(reverse('delete_customer', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Customer.objects.filter(pk=self.customer.pk).exists())

        response = self.client.post(reverse('delete_customer', args=[self.customer.pk]))
        self.assertRedirects(response, reverse('customers_index'))
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())

    def customer_data(self, **overrides):
        data = {
            'name': 'Customer',
            'phone': '123',
            'gender': 'Other',
            'marital_status': '',
            'birthday': '',
            'city': '',
            'state': '',
            'street': '',
            'house_number': '',
        }
        data.update(overrides)
        return data

    def test_all_customer_pages_require_login(self):
        self.client.logout()
        urls = [
            reverse('customers_index'),
            reverse('create_customer'),
            reverse('view_customer', args=[self.customer.pk]),
            reverse('edit_customer', args=[self.customer.pk]),
            reverse('delete_customer', args=[self.customer.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_create_customer_ignores_statistic_fields(self):
        response = self.client.post(
            reverse('create_customer'),
            self.customer_data(
                name='New Customer',
                total_orders='99',
                total_spent='999.99',
            ),
        )

        self.assertRedirects(response, reverse('customers_index'))
        customer = Customer.objects.get(name='New Customer')
        self.assertEqual(customer.total_orders, 0)
        self.assertEqual(customer.total_spent, Decimal('0.00'))

    def test_customer_details_links_to_prefilled_order(self):
        response = self.client.get(reverse('view_customer', args=[self.customer.pk]))

        self.assertContains(
            response,
            f"{reverse('create_order')}?customer={self.customer.pk}",
        )

    def test_delete_customer_preserves_orders_without_customer(self):
        order = Order.objects.create(
            order_number='ORD-1',
            customer=self.customer,
            status=OrderStatus.COMPLETED,
        )

        response = self.client.post(reverse('delete_customer', args=[self.customer.pk]))

        self.assertRedirects(response, reverse('customers_index'))
        order.refresh_from_db()
        self.assertIsNone(order.customer)

    def test_customers_are_ordered_by_name(self):
        Customer.objects.create(name='Zulu Customer', phone='123')
        Customer.objects.create(name='Alpha Customer', phone='123')

        response = self.client.get(reverse('customers_index'))

        names = [customer.name for customer in response.context['customers']]
        self.assertEqual(names, ['Alpha Customer', 'Customer', 'Zulu Customer'])

    def test_missing_customer_returns_404(self):
        response = self.client.get(reverse('view_customer', args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('edit_customer', args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('delete_customer', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_customer_requires_name(self):
        response = self.client.post(
            reverse('create_customer'),
            self.customer_data(name=''),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
        self.assertEqual(Customer.objects.count(), 1)
