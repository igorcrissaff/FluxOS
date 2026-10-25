from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.orders.models import Order, OrderStatus
from apps.stock.models import Product

from .context_processors import alerts


class AlertContextProcessorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='staff',
            password='testpass123',
        )

    def request_for(self, user):
        request = RequestFactory().get('/')
        request.user = user
        return request

    def test_anonymous_user_has_no_alerts(self):
        context = alerts(self.request_for(AnonymousUser()))

        self.assertEqual(context, {})

    def test_alert_counts_only_available_low_stock_and_pending_orders(self):
        low_stock = Product.objects.create(
            sku='SKU-LOW',
            name='Low Stock',
            price=Decimal('10.00'),
            quantity=1,
            low_stock_threshold=5,
            available=True,
        )
        Product.objects.create(
            sku='SKU-HIDDEN',
            name='Hidden Low Stock',
            price=Decimal('10.00'),
            quantity=0,
            low_stock_threshold=5,
            available=False,
        )
        Product.objects.create(
            sku='SKU-HEALTHY',
            name='Healthy Stock',
            price=Decimal('10.00'),
            quantity=10,
            low_stock_threshold=5,
            available=True,
        )
        Order.objects.create(order_number='PENDING', status=OrderStatus.PENDING)
        Order.objects.create(order_number='COMPLETED', status=OrderStatus.COMPLETED)

        context = alerts(self.request_for(self.user))

        self.assertEqual(context['low_stock_count'], 1)
        self.assertEqual(context['pending_order_alerts'], 1)
        self.assertEqual(context['alert_count'], 2)
        self.assertEqual(list(context['low_stock_alerts']), [low_stock])

    def test_low_stock_alert_list_is_limited_to_five(self):
        for index in range(6):
            Product.objects.create(
                sku=f'SKU-{index}',
                name=f'Low Stock {index}',
                price=Decimal('10.00'),
                quantity=index,
                low_stock_threshold=5,
                available=True,
            )

        context = alerts(self.request_for(self.user))

        self.assertEqual(context['low_stock_count'], 6)
        self.assertEqual(len(list(context['low_stock_alerts'])), 5)


class AuthFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='staff',
            password='testpass123',
        )

    def test_login_page_is_available_anonymously(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_logout_requires_post(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_post_ends_session(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(
            response,
            settings.LOGOUT_REDIRECT_URL,
            fetch_redirect_response=False,
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_language_switch_stores_locale_cookie(self):
        response = self.client.post(
            reverse('set_language'),
            {'language': 'pt-br', 'next': '/'},
        )

        self.assertRedirects(response, '/', fetch_redirect_response=False)
        self.assertEqual(
            self.client.cookies[settings.LANGUAGE_COOKIE_NAME].value,
            'pt-br',
        )
