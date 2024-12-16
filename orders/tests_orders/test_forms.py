from django.test import TestCase, Client
from django.urls import reverse

from orders.forms import OrderForm
from customers.models import Customer


class OrderFormTests(TestCase):
    """Тесты для формы создания заказов."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('create_order')
        self.customer = Customer.objects.create(email='test@example.ru')

    def test_create_order_with_valid_data(self):
        form_data = {
            'email': 'test@example.ru',
            'robot_serial': 'R2-D2'
            }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid_email(self):
        form_data = {
            'email': 'invalid_email',
            'robot_serial': 'R2-D2'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_order_form_invalid_robot_serial(self):
        form_data = {
            'email': 'test@example.com',
            'robot_serial': 'X2-D2'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('robot_serial', form.errors)
