from django.test import TestCase
from django.urls import reverse

from ..forms import RobotForm
from .test_views import VALID_DATA


class RobotFormTests(TestCase):
    def setUp(self):
        self.url = reverse('robot_creation_without_csrf')
        self.valid_data = VALID_DATA

    def test_robot_form__with_valid_data(self):
        form = RobotForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        robot = form.save()
        self.assertEqual(robot.model, 'X5')
        self.assertEqual(robot.version, 'LT')

    def test_robot_form_with_invalid_model(self):
        invalid_data = {
            'model': 'X2',
            'version': 'LT',
            'created': '2023-01-01 00:00:01'
        }
        form = RobotForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This model is not allowed', form.errors['__all__'])

    def test_robot_form_with_invalid_created(self):
        invalid_data = {
            'model': 'X5',
            'version': 'LT',
            'created': ''
        }
        form = RobotForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('created', form.errors)
