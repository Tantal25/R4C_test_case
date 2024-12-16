from django.test import TestCase
from django.core import mail

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


class OrderReadySignalTests(TestCase):
    """Тесты на сигнал готовности заказа."""

    def setUp(self):
        self.customer = Customer.objects.create(email='customer@example.com')
        self.order = Order.objects.create(
            customer=self.customer,
            robot_serial='R2-D2')

    def test_send_email_order_ready(self):
        Robot.objects.create(
            serial='R2-D2',
            model='R2',
            version='D2',
            created='2023-01-01 00:00:00'
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.customer.email])

        order = Order.objects.get(id=self.order.id)
        self.assertTrue(order.in_process)
