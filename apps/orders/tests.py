from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.customers.models import Customer
from apps.stock.models import Product

from .models import Order, OrderItem, OrderStatus
from .services import update_customer_stats


class OrderModelTest(TestCase):
    def test_total_and_subtotal(self):
        customer = Customer.objects.create(name='Customer', phone='123')
        product = Product.objects.create(
            sku='SKU-1',
            name='Product',
            price=Decimal('10.00'),
            quantity=10,
        )
        order = Order.objects.create(order_number='ORD-1', customer=customer)
        item = OrderItem.objects.create(order=order, product=product, quantity=2)

        self.assertEqual(item.subtotal, Decimal('20.00'))
        self.assertEqual(order.total, Decimal('20.00'))

    def test_customer_stats_ignore_canceled_and_returned_orders(self):
        customer = Customer.objects.create(name='Customer', phone='123')
        Order.objects.create(
            order_number='PENDING',
            customer=customer,
            status=OrderStatus.PENDING,
        )
        Order.objects.create(
            order_number='CANCELED',
            customer=customer,
            status=OrderStatus.CANCELED,
        )

        update_customer_stats(customer)
        customer.refresh_from_db()

        self.assertEqual(customer.total_orders, 1)
        self.assertEqual(customer.total_spent, Decimal('0.00'))

    def test_customer_stats_include_completed_and_shipped_revenue(self):
        customer = Customer.objects.create(name='Customer', phone='123')
        product = Product.objects.create(
            sku='SKU-1',
            name='Product',
            price=Decimal('10.00'),
            quantity=10,
        )
        completed = Order.objects.create(
            order_number='COMPLETED',
            customer=customer,
            status=OrderStatus.COMPLETED,
        )
        OrderItem.objects.create(order=completed, product=product, quantity=2)
        shipped = Order.objects.create(
            order_number='SHIPPED',
            customer=customer,
            status=OrderStatus.SHIPPED,
        )
        OrderItem.objects.create(order=shipped, product=product, quantity=3)
        returned = Order.objects.create(
            order_number='RETURNED',
            customer=customer,
            status=OrderStatus.RETURNED,
        )
        OrderItem.objects.create(order=returned, product=product, quantity=5)

        update_customer_stats(customer)
        customer.refresh_from_db()

        self.assertEqual(customer.total_orders, 2)
        self.assertEqual(customer.total_spent, Decimal('50.00'))

    def test_customer_stats_ignore_missing_customer(self):
        self.assertIsNone(update_customer_stats(None))

    def test_order_string_representation(self):
        customer = Customer.objects.create(name='Customer', phone='123')
        order = Order.objects.create(order_number='ORD-1', customer=customer)
        order_without_customer = Order.objects.create(order_number='ORD-2')

        self.assertEqual(str(order), 'Order ORD-1 for Customer')
        self.assertEqual(str(order_without_customer), 'Order ORD-2 for Unknown Customer')

    def test_order_item_string_and_subtotal_without_product(self):
        customer = Customer.objects.create(name='Customer', phone='123')
        product = Product.objects.create(
            sku='SKU-1',
            name='Product',
            price=Decimal('10.00'),
            quantity=10,
        )
        order = Order.objects.create(order_number='ORD-1', customer=customer)
        item = OrderItem.objects.create(order=order, product=product, quantity=2)

        self.assertEqual(str(item), '2 x Product for Order ORD-1')
        product.delete()
        item.refresh_from_db()
        self.assertEqual(str(item), '2 x Deleted Product for Order ORD-1')
        self.assertEqual(item.subtotal, Decimal('0.00'))


class OrderViewTest(TestCase):
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
            quantity=10,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def order_data(self, **overrides):
        data = {
            'order_number': 'ORD-1',
            'customer': self.customer.pk,
            'status': OrderStatus.PENDING,
            'orderitem_set-TOTAL_FORMS': '1',
            'orderitem_set-INITIAL_FORMS': '0',
            'orderitem_set-MIN_NUM_FORMS': '1',
            'orderitem_set-MAX_NUM_FORMS': '1000',
            'orderitem_set-0-product': self.product.pk,
            'orderitem_set-0-quantity': '2',
            'orderitem_set-0-id': '',
        }
        data.update(overrides)
        return data

    def test_order_pages_require_login(self):
        self.client.logout()
        response = self.client.get(reverse('orders_index'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('orders_index')}")

    def test_create_order_with_items(self):
        response = self.client.post(reverse('create_order'), self.order_data())
        order = Order.objects.get(order_number='ORD-1')

        self.assertRedirects(response, reverse('view_order', args=[order.pk]))
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order.total, Decimal('20.00'))

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_orders, 1)
        self.assertEqual(self.customer.total_spent, Decimal('0.00'))

    def test_create_order_requires_at_least_one_item(self):
        response = self.client.post(
            reverse('create_order'),
            self.order_data(**{
                'orderitem_set-TOTAL_FORMS': '0',
                'orderitem_set-0-product': '',
                'orderitem_set-0-quantity': '',
            }),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.filter(order_number='ORD-1').exists())
        self.assertTrue(response.context['formset'].non_form_errors())

    def test_order_item_quantity_must_be_positive(self):
        response = self.client.post(
            reverse('create_order'),
            self.order_data(**{'orderitem_set-0-quantity': '0'}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.filter(order_number='ORD-1').exists())
        self.assertIn('quantity', response.context['formset'].forms[0].errors)

    def test_edit_order_updates_customer_stats(self):
        order = Order.objects.create(
            order_number='ORD-1',
            customer=self.customer,
            status=OrderStatus.PENDING,
        )
        item = OrderItem.objects.create(order=order, product=self.product, quantity=2)

        response = self.client.post(
            reverse('edit_order', args=[order.pk]),
            {
                'order_number': 'ORD-1',
                'customer': self.customer.pk,
                'status': OrderStatus.COMPLETED,
                'orderitem_set-TOTAL_FORMS': '1',
                'orderitem_set-INITIAL_FORMS': '1',
                'orderitem_set-MIN_NUM_FORMS': '1',
                'orderitem_set-MAX_NUM_FORMS': '1000',
                'orderitem_set-0-id': item.pk,
                'orderitem_set-0-product': self.product.pk,
                'orderitem_set-0-quantity': '2',
            },
        )

        self.assertRedirects(response, reverse('view_order', args=[order.pk]))
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.COMPLETED)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_orders, 1)
        self.assertEqual(self.customer.total_spent, Decimal('20.00'))

    def test_delete_order_updates_customer_stats(self):
        order = Order.objects.create(
            order_number='ORD-1',
            customer=self.customer,
            status=OrderStatus.COMPLETED,
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=2)
        update_customer_stats(self.customer)

        response = self.client.post(reverse('delete_order', args=[order.pk]))

        self.assertRedirects(response, reverse('orders_index'))
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_orders, 0)
        self.assertEqual(self.customer.total_spent, Decimal('0.00'))

    def test_order_status_filter(self):
        pending = Order.objects.create(
            order_number='PENDING',
            customer=self.customer,
            status=OrderStatus.PENDING,
        )
        Order.objects.create(
            order_number='COMPLETED',
            customer=self.customer,
            status=OrderStatus.COMPLETED,
        )

        response = self.client.get(reverse('orders_index'), {'status': OrderStatus.PENDING})

        self.assertEqual(list(response.context['orders']), [pending])
        self.assertEqual(response.context['status'], OrderStatus.PENDING)

    def test_order_details_renders_items(self):
        order = Order.objects.create(order_number='ORD-1', customer=self.customer)
        OrderItem.objects.create(order=order, product=self.product, quantity=2)

        response = self.client.get(reverse('view_order', args=[order.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORD-1')
        self.assertContains(response, 'Product')
        self.assertContains(response, 'R$20.00')

    def test_all_order_pages_require_login(self):
        order = Order.objects.create(order_number='ORD-1', customer=self.customer)
        self.client.logout()
        urls = [
            reverse('orders_index'),
            reverse('create_order'),
            reverse('view_order', args=[order.pk]),
            reverse('edit_order', args=[order.pk]),
            reverse('delete_order', args=[order.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_create_order_prefills_customer(self):
        response = self.client.get(
            reverse('create_order'),
            {'customer': self.customer.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.context['form'].initial['customer']),
            str(self.customer.pk),
        )

    def test_create_order_without_customer(self):
        response = self.client.post(
            reverse('create_order'),
            self.order_data(customer=''),
        )

        order = Order.objects.get(order_number='ORD-1')
        self.assertRedirects(response, reverse('view_order', args=[order.pk]))
        self.assertIsNone(order.customer)

    def test_create_order_rejects_duplicate_order_number(self):
        Order.objects.create(order_number='ORD-1', customer=self.customer)

        response = self.client.post(reverse('create_order'), self.order_data())

        self.assertEqual(response.status_code, 200)
        self.assertIn('order_number', response.context['form'].errors)
        self.assertEqual(Order.objects.filter(order_number='ORD-1').count(), 1)

    def test_edit_order_moves_customer_stats(self):
        other_customer = Customer.objects.create(name='Other Customer', phone='456')
        order = Order.objects.create(
            order_number='ORD-1',
            customer=self.customer,
            status=OrderStatus.COMPLETED,
        )
        item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        update_customer_stats(self.customer)

        response = self.client.post(
            reverse('edit_order', args=[order.pk]),
            {
                'order_number': 'ORD-1',
                'customer': other_customer.pk,
                'status': OrderStatus.COMPLETED,
                'orderitem_set-TOTAL_FORMS': '1',
                'orderitem_set-INITIAL_FORMS': '1',
                'orderitem_set-MIN_NUM_FORMS': '1',
                'orderitem_set-MAX_NUM_FORMS': '1000',
                'orderitem_set-0-id': item.pk,
                'orderitem_set-0-product': self.product.pk,
                'orderitem_set-0-quantity': '2',
            },
        )

        self.assertRedirects(response, reverse('view_order', args=[order.pk]))
        self.customer.refresh_from_db()
        other_customer.refresh_from_db()
        self.assertEqual(self.customer.total_orders, 0)
        self.assertEqual(self.customer.total_spent, Decimal('0.00'))
        self.assertEqual(other_customer.total_orders, 1)
        self.assertEqual(other_customer.total_spent, Decimal('20.00'))

    def test_delete_order_requires_post(self):
        order = Order.objects.create(order_number='ORD-1', customer=self.customer)

        response = self.client.get(reverse('delete_order', args=[order.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Order.objects.filter(pk=order.pk).exists())

    def test_delete_order_without_customer(self):
        order = Order.objects.create(order_number='ORD-1')

        response = self.client.post(reverse('delete_order', args=[order.pk]))

        self.assertRedirects(response, reverse('orders_index'))
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())

    def test_invalid_status_filter_is_ignored(self):
        pending = Order.objects.create(
            order_number='PENDING',
            customer=self.customer,
            status=OrderStatus.PENDING,
        )
        completed = Order.objects.create(
            order_number='COMPLETED',
            customer=self.customer,
            status=OrderStatus.COMPLETED,
        )

        response = self.client.get(reverse('orders_index'), {'status': 'Invalid'})

        self.assertEqual(response.context['status'], '')
        self.assertIsNone(response.context['status_label'])
        self.assertEqual(list(response.context['orders']), [completed, pending])

    def test_missing_order_returns_404(self):
        response = self.client.get(reverse('view_order', args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('edit_order', args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('delete_order', args=[9999]))
        self.assertEqual(response.status_code, 404)
