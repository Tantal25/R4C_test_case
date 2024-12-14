import json

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Robot


VALID_DATA = {
    "model": "R2",
    "version": "D2",
    "created": "2022-12-31 23:59:59"
    }


class RobotCreationAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('robot_creation_API')
        self.valid_data = VALID_DATA

    def test_robot_creation_with_valid_data(self):
        response = self.client.post(
            self.url,
            json.dumps(self.valid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['Результат'],
            'Данные о производстве робота приняты'
        )
        self.assertEqual(Robot.objects.count(), 1)

        robot = Robot.objects.first()
        self.assertEqual(robot.model, 'R2')
        self.assertEqual(robot.version, 'D2')
        self.assertEqual(robot.serial, 'R2-D2')

    def test_robot_creation_with_forbidden_model(self):
        invalid_data = {
            "model": "D5",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
            }
        response = self.client.post(
            self.url,
            json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn(
            'Эта модель робота не разрешена',
            response.json()['error']['__all__']
        )

    def test_robot_creation_with_invalid_version(self):
        invalid_data = {
            "model": "R2",
            "version": "Invalid",
            "created": "2022-12-31 23:59:59"
            }
        response = self.client.post(
            self.url,
            json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_robot_creation_with_invalid_json(self):
        response = self.client.post(
            self.url,
            data='',
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(
            response.json()['error'],
            'Некорректный формат, передайте данные в формате JSON.'
            )
