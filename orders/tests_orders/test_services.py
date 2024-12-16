from django.test import TestCase

from orders.models import Order
from customers.models import Customer
from orders.services import (
    find_unprocessed_order, db_order_creation,
    change_order_in_process_status
    )


class OrdersServicesTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(email='customer@example.com')

    def test_find_unprocessed_order(self):
        order = Order.objects.create(
            customer=self.customer,
            robot_serial='R2-D2')
        found_order = find_unprocessed_order('R2-D2')
        self.assertEqual(found_order, order)

    def test_db_order_creation(self):
        # Данные для создания заказа
        data = {'robot_serial': 'R2-D2'}

        # Создаем заказ
        db_order_creation(data, self.customer)

        order = Order.objects.get(customer=self.customer, robot_serial='R2-D2')
        self.assertIsNotNone(order)
        self.assertEqual(order.robot_serial, 'R2-D2')
        self.assertEqual(order.customer, self.customer)

    def test_order_process_status_and_change_status(self):
        order = Order.objects.create(
            customer=self.customer,
            robot_serial='R2-D2')

        self.assertFalse(order.in_process)
        change_order_in_process_status(order)
        self.assertTrue(order.in_process)
