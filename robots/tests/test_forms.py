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
        form = JsonForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        robot = form.save()
        self.assertEqual(robot.model, 'R2')
        self.assertEqual(robot.version, 'D2')

    def test_JsonForm_with_invalid_model(self):
        invalid_data = {
            'model': 'X2',
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }
        form = JsonForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Эта модель робота не разрешена', form.errors['__all__'])

    def test_JsonForm_with_invalid_created(self):
        invalid_data = {
            'model': 'R2',
            'version': 'D2',
            'created': ''
        }

        form = JsonForm(json.dumps(invalid_data))
        self.assertFalse(form.is_valid())
        self.assertIn('created', form.errors)


class RobotFormTests(TestCase):

    def setUp(self):
        self.url = reverse('robot_creation_API')
        self.valid_data = VALID_DATA

    def test_robot_form_with_valid_data(self):
        form = RobotForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        robot = form.save()
        self.assertEqual(robot.model, 'R2')
        self.assertEqual(robot.version, 'D2')

    def test_robot_form_with_invalid_model(self):
        invalid_data = {
            "model": "Invalid",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        form = RobotForm(invalid_data)
        with self.assertRaises(KeyError):
            form.is_valid()
