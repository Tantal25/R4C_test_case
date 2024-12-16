from django.test import TestCase, Client
from django.urls import reverse

from customers.models import Customer


class CreateCustomersTests(TestCase):
    """Тесты на создание пользователей."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('create_customer')
        self.customer = Customer.objects.create(email='valid@example.ru')

    def test_create_customer(self):
        response = self.client.post(self.url, {'email': 'Test01@example.ru'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Customer.objects.filter(
            email='Test01@example.ru').exists())

    def test_create_customer_already_exist(self):
        customers_count = Customer.objects.count()
        response = self.client.post(self.url, {'email': 'valid@example.ru'})

        self.assertEqual(Customer.objects.count(), customers_count)
        self.assertContains(
            response,
            'Пользователь с таким email уже существует.',
            status_code=400
            )
