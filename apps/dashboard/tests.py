from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.orders.services import update_customer_stats
from apps.stock.models import Product

from .forms import ProfileForm


class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='staff',
            password='testpass123',
            is_staff=True,
        )
        cls.customer = Customer.objects.create(name='Customer', phone='123')
        cls.product = Product.objects.create(
            sku='SKU-1',
            name='Product',
            price=Decimal('10.00'),
            quantity=1,
            low_stock_threshold=5,
            available=True,
        )

        completed = Order.objects.create(
            order_number='COMPLETED',
            customer=cls.customer,
            status=OrderStatus.COMPLETED,
        )
        OrderItem.objects.create(order=completed, product=cls.product, quantity=2)

        shipped = Order.objects.create(
            order_number='SHIPPED',
            customer=cls.customer,
            status=OrderStatus.SHIPPED,
        )
        OrderItem.objects.create(order=shipped, product=cls.product, quantity=3)

        Order.objects.create(
            order_number='PENDING',
            customer=cls.customer,
            status=OrderStatus.PENDING,
        )

        previous_year_date = timezone.now().replace(
            year=timezone.localdate().year - 1,
            month=6,
            day=1,
        )
        old_order = Order.objects.create(
            order_number='OLD',
            customer=cls.customer,
            status=OrderStatus.COMPLETED,
        )
        Order.objects.filter(pk=old_order.pk).update(order_date=previous_year_date)
        update_customer_stats(cls.customer)

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_metrics(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthly_revenue'], Decimal('50.00'))
        self.assertEqual(response.context['annual_revenue'], Decimal('50.00'))
        self.assertEqual(response.context['pending_orders_count'], 1)
        self.assertEqual(response.context['low_stock_count'], 1)
        self.assertEqual(response.context['alert_count'], 2)

    def test_dashboard_lists_recent_orders_and_low_stock(self):
        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'COMPLETED')
        self.assertContains(response, 'PENDING')
        self.assertContains(response, 'Product')

    def test_profile_form_only_exposes_safe_fields(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProfileForm)
        self.assertEqual(
            list(response.context['form'].fields.keys()),
            ['username', 'first_name', 'last_name', 'email'],
        )

    def test_profile_update_ignores_permission_fields(self):
        response = self.client.post(
            reverse('profile'),
            {
                'username': 'updated',
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': 'updated@example.com',
                'is_staff': '',
                'is_active': '',
                'is_superuser': '',
            },
        )

        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

    def test_profile_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_rejects_duplicate_username(self):
        other = User.objects.create_user(
            username='other',
            password='testpass123',
        )

        response = self.client.post(
            reverse('profile'),
            {
                'username': other.username,
                'first_name': '',
                'last_name': '',
                'email': '',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'staff')

    def test_low_stock_excludes_unavailable_products(self):
        Product.objects.create(
            sku='SKU-UNAVAILABLE',
            name='Unavailable Low Stock',
            price=Decimal('10.00'),
            quantity=0,
            low_stock_threshold=5,
            available=False,
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['low_stock_count'], 1)
        self.assertEqual(list(response.context['low_stock_products']), [self.product])

    def test_revenue_excludes_non_revenue_statuses(self):
        for number, status in [
            ('CANCELED-REVENUE', OrderStatus.CANCELED),
            ('RETURNED-REVENUE', OrderStatus.RETURNED),
        ]:
            order = Order.objects.create(
                order_number=number,
                customer=self.customer,
                status=status,
            )
            OrderItem.objects.create(order=order, product=self.product, quantity=10)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['monthly_revenue'], Decimal('50.00'))
        self.assertEqual(response.context['annual_revenue'], Decimal('50.00'))

    def test_top_customers_are_ordered_and_limited(self):
        for index in range(6, 12):
            Customer.objects.create(
                name=f'Top Customer {index}',
                phone='123',
                total_spent=Decimal(index * 10),
            )

        response = self.client.get(reverse('dashboard'))

        top_customers = list(response.context['top_customers'])
        self.assertEqual(len(top_customers), 5)
        self.assertEqual(
            [customer.total_spent for customer in top_customers],
            [
                Decimal('110.00'),
                Decimal('100.00'),
                Decimal('90.00'),
                Decimal('80.00'),
                Decimal('70.00'),
            ],
        )

    def test_recent_orders_are_limited_to_five(self):
        for index in range(3):
            Order.objects.create(
                order_number=f'EXTRA-{index}',
                customer=self.customer,
            )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(len(response.context['recent_orders']), 5)


class EmptyDashboardTest(TestCase):
    def test_dashboard_handles_empty_database(self):
        user = User.objects.create_user(username='staff', password='testpass123')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthly_revenue'], Decimal('0.00'))
        self.assertEqual(response.context['annual_revenue'], Decimal('0.00'))
        self.assertEqual(response.context['pending_orders_count'], 0)
        self.assertEqual(response.context['low_stock_count'], 0)
        self.assertEqual(list(response.context['recent_orders']), [])
        self.assertEqual(list(response.context['top_customers']), [])
