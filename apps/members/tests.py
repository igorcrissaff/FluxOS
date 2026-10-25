from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import MemberForm


class MemberFormTest(TestCase):
    def member_data(self, **overrides):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'is_active': 'on',
            'is_staff': 'on',
        }
        data.update(overrides)
        return data

    def test_creating_requires_passwords(self):
        form = MemberForm(data=self.member_data(), creating=True)

        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_non_superuser_form_hides_staff_field(self):
        form = MemberForm(creating=True, can_manage_staff=False)

        self.assertNotIn('is_staff', form.fields)

    def test_weak_password_is_rejected(self):
        form = MemberForm(
            data=self.member_data(
                password1='123',
                password2='123',
            ),
            creating=True,
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)


class MemberViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username='staff',
            password='testpass123',
            is_staff=True,
        )
        cls.other_staff = User.objects.create_user(
            username='other',
            password='testpass123',
            is_staff=True,
        )
        cls.regular = User.objects.create_user(
            username='regular',
            password='testpass123',
        )
        cls.superuser = User.objects.create_superuser(
            username='admin',
            password='testpass123',
            email='admin@example.com',
        )

    def test_non_staff_cannot_access_user_management(self):
        self.client.force_login(self.regular)
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_access_user_management(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)

    def test_staff_cannot_grant_staff_status(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse('create_user'),
            {
                'username': 'newuser',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'new@example.com',
                'is_active': 'on',
                'is_staff': 'on',
                'password1': 'A-very-strong-pass-123',
                'password2': 'A-very-strong-pass-123',
            },
        )
        self.assertRedirects(response, reverse('users_index'))
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('A-very-strong-pass-123'))

    def test_password_mismatch_does_not_create_user(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse('create_user'),
            {
                'username': 'newuser',
                'first_name': '',
                'last_name': '',
                'email': '',
                'is_active': 'on',
                'password1': 'A-very-strong-pass-123',
                'password2': 'Different-pass-456',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_staff_cannot_deactivate_own_account(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse('edit_user', args=[self.staff.pk]),
            {
                'username': self.staff.username,
                'first_name': '',
                'last_name': '',
                'email': '',
                'password1': '',
                'password2': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_active', response.context['form'].errors)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.is_active)

    def test_staff_cannot_delete_own_account(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('delete_user', args=[self.staff.pk]))
        self.assertRedirects(response, reverse('users_index'))
        self.assertTrue(User.objects.filter(pk=self.staff.pk).exists())

    def test_staff_cannot_edit_superuser(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('edit_user', args=[self.superuser.pk]))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_delete_regular_user(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('delete_user', args=[self.regular.pk]))
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(User.objects.filter(pk=self.regular.pk).exists())

    def test_delete_user_requires_post(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('delete_user', args=[self.regular.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(User.objects.filter(pk=self.regular.pk).exists())

    def test_all_user_pages_require_login(self):
        urls = [
            reverse('users_index'),
            reverse('create_user'),
            reverse('edit_user', args=[self.regular.pk]),
            reverse('delete_user', args=[self.regular.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_non_staff_cannot_access_user_pages(self):
        self.client.force_login(self.regular)
        urls = [
            reverse('create_user'),
            reverse('edit_user', args=[self.other_staff.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse('delete_user', args=[self.other_staff.pk]))
        self.assertEqual(response.status_code, 403)

    def test_staff_cannot_delete_superuser(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('delete_user', args=[self.superuser.pk]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=self.superuser.pk).exists())

    def test_superuser_can_create_staff_user(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse('create_user'),
            {
                'username': 'newstaff',
                'first_name': 'New',
                'last_name': 'Staff',
                'email': 'newstaff@example.com',
                'is_active': 'on',
                'is_staff': 'on',
                'password1': 'A-very-strong-pass-123',
                'password2': 'A-very-strong-pass-123',
            },
        )

        self.assertRedirects(response, reverse('users_index'))
        user = User.objects.get(username='newstaff')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password('A-very-strong-pass-123'))

    def test_staff_edit_ignores_injected_staff_flag(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse('edit_user', args=[self.regular.pk]),
            {
                'username': self.regular.username,
                'first_name': 'Updated',
                'last_name': 'User',
                'email': 'updated@example.com',
                'is_active': 'on',
                'is_staff': 'on',
                'password1': '',
                'password2': '',
            },
        )

        self.assertRedirects(response, reverse('users_index'))
        self.regular.refresh_from_db()
        self.assertFalse(self.regular.is_staff)
        self.assertEqual(self.regular.first_name, 'Updated')

    def test_edit_user_without_password_preserves_password(self):
        original_password = self.regular.password
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse('edit_user', args=[self.regular.pk]),
            {
                'username': self.regular.username,
                'first_name': '',
                'last_name': '',
                'email': '',
                'is_active': 'on',
                'password1': '',
                'password2': '',
            },
        )

        self.assertRedirects(response, reverse('users_index'))
        self.regular.refresh_from_db()
        self.assertEqual(self.regular.password, original_password)
        self.assertTrue(self.regular.check_password('testpass123'))

    def test_missing_user_returns_404(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('edit_user', args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('delete_user', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_users_are_ordered_by_username(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('users_index'))

        usernames = [user.username for user in response.context['users']]
        self.assertEqual(usernames, ['admin', 'other', 'regular', 'staff'])
