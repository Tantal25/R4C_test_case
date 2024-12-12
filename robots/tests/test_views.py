import json

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Robot


VALID_DATA = {
    'model': 'X5',
    'version': 'LT',
    'created': '2023-01-01 00:00:01'
    }


class RobotCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('robot_creation')
        self.valid_data = VALID_DATA

    def test_robot_creation_with_valid_data(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Robot.objects.exists())

    def test_robot_creation_with_invalid_model(self):
        invalid_data = {
            'model': 'X2',
            'version': 'LT',
            'created': '2023-01-01 00:00:01'
        }
        self.client.post(self.url, invalid_data)
        self.assertFalse(Robot.objects.exists())

    def test_robot_creation_with_invalid_datetime(self):
        invalid_data = {
            'model': 'X5',
            'version': 'LT',
            'created': ''
        }
        self.client.post(self.url, invalid_data)
        self.assertFalse(Robot.objects.exists())


class RobotCreationWithoutCSRFTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('robot_creation_without_csrf')
        self.valid_data = VALID_DATA

    def test_robot_creation__with_valid_data(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Robot.objects.exists())

    def test_robot_creation_with_invalid_json(self):
        response = self.client.post(
            self.url,
            data='',
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Неправильный формат JSON')
