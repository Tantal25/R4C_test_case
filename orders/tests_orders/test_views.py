from django.test import TestCase, Client
from django.urls import reverse

from orders.models import Order
from customers.models import Customer


class CreateOrderTests(TestCase):
    """Тесты на создание заказов."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('create_order')
        self.customer = Customer.objects.create(email='test@example.ru')

    def test_create_order_with_valid_data(self):
        response = self.client.post(
            self.url,
            {'email': self.customer.email,
             'robot_serial': 'R2-D2'}
             )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заказ на робота R2-D2 принят.')
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())

    def test_create_order_with_invalid_email(self):
        response = self.client.post(
            self.url,
            {'email': "Invalid@example.ru",
             'robot_serial': 'R2-D2'}
             )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(
            response,
            ('Пользователь с таким email не найден, '
             'пожалуйста зарегистрируйтесь прежде чем сделать заказ'),
            status_code=400
             )

    def test_create_order_with_invalid_robot_serial_model(self):
        response = self.client.post(
            self.url,
            {'email': self.customer.email,
             'robot_serial': 'R8-D2'}
             )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(
            response,
            'Эта модель робота не разрешена',
            status_code=400
            )

    def test_create_order_with_invalid_robot_serial_version(self):
        response = self.client.post(
            self.url,
            {'email': self.customer.email,
             'robot_serial': 'R2-D9'}
             )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(
            response,
            'Эта версия робота не разрешена',
            status_code=400
            )
