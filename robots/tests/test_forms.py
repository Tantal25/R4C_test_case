import json

from django.test import TestCase
from django.urls import reverse

from ..forms import JsonForm, RobotForm
from .test_views import VALID_DATA


class JsonFormTests(TestCase):
    def setUp(self):
        self.url = reverse('json_robot_creation')
        self.valid_data = VALID_DATA

    def test_JsonForm_with_valid_data(self):
        form = JsonForm({'json_data': json.dumps(self.valid_data)})
        self.assertTrue(form.is_valid())

    def test_JsonForm_with_forbidden_model(self):
        invalid_data = {
            'model': 'X2',
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }
        form = JsonForm({'json_data': json.dumps(invalid_data)})
        self.assertFalse(form.is_valid())
        self.assertIn('Эта модель робота не разрешена', form.errors['__all__'])

    def test_JsonForm_without_model_field(self):
        invalid_data = {
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }
        form = JsonForm({'json_data': json.dumps(invalid_data)})
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Передана некорректная модель робота',
            form.errors['__all__']
        )

    def test_JsonForm_with_invalid_model(self):
        invalid_data = {
            'model': 'Invalid',
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }
        form = JsonForm({'json_data': json.dumps(invalid_data)})
        self.assertFalse(form.is_valid())
        self.assertIn('Эта модель робота не разрешена', form.errors['__all__'])


class RobotFormTests(TestCase):

    def setUp(self):
        self.url = reverse('robot_creation_API')
        self.valid_data = VALID_DATA

    def test_RobotForm_with_valid_data(self):
        form = RobotForm(self.valid_data)
        self.assertTrue(form.is_valid())
        robot = form.save()
        self.assertEqual(robot.model, 'R2')
        self.assertEqual(robot.version, 'D2')

    def test_RobotForm_with_invalid_model(self):
        invalid_data = {
            "model": "Invalid",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        form = RobotForm(invalid_data)
        self.assertIn(
            'Передана некорректная модель робота',
            form.errors['__all__']
        )

    def test_RobotForm_with_forbidden_model(self):
        invalid_data = {
            'model': 'X2',
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }
        form = RobotForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Эта модель робота не разрешена', form.errors['__all__'])

    def test_RobotForm_with_invalid_version(self):
        invalid_data = {
            "model": "R2",
            "version": "D25555",
            "created": "2022-12-31 23:59:59"
        }
        form = RobotForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value has at most 2 characters',
            form.errors['version'][0]
        )

    def test_RobotForm_without_version(self):
        invalid_data = {
            "model": "R2",
            "created": "2022-12-31 23:59:59"
        }
        form = RobotForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'This field is required',
            form.errors['version'][0]
        )

    def test_RobotForm_with_empty_created(self):
        invalid_data = {
            'model': 'R2',
            'version': 'D2',
            'created': ''
        }
        form = RobotForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['created'])

    def test_RobotForm_with_invalid_created(self):
        invalid_data = {
            'model': 'R2',
            'version': 'D2',
            'created': 'Some_invalid_string'
        }
        form = RobotForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid date/time.', form.errors['created'])
