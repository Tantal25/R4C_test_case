from django.test import TestCase
from django.utils import timezone

from robots.models import Robot
from robots.services import (
    db_robot_creation,
    get_robots_created_for_week,
    prepare_empty_excel_workbook,
    prepare_robot_data_before_writing
)


class RobotFunctionsTests(TestCase):
    """Тесты к сервисным функциям создания роботов."""

    def setUp(self):
        self.robot_data = {
            'model': 'R2',
            'version': 'D2',
            'created': timezone.now()
        }

    def test_db_robot_creation(self):
        """Тест функции создания робота в БД."""
        result = db_robot_creation(self.robot_data)
        self.assertEqual(Robot.objects.count(), 1)
        robot = Robot.objects.filter(**self.robot_data).first()
        self.assertEqual(
            result,
            'Данные о производстве робота модели R2, версии D2 приняты'
            )
        self.assertEqual(robot.model, self.robot_data['model'])
        self.assertEqual(robot.version, self.robot_data['version'])

    def test_get_robots_created_for_week(self):
        """Тест функции, получающей выборку роботов за неделю."""
        # Создаем роботов, которые будут в выборке
        db_robot_creation(self.robot_data)
        db_robot_creation(self.robot_data)

        # Создаем робота, который будет вне выборки
        second_robot_data = self.robot_data.copy()
        second_robot_data['created'] = timezone.now() - timezone.timedelta(
            weeks=2
            )
        db_robot_creation(second_robot_data)

        # Получаем роботов, созданных за неделю
        robots = get_robots_created_for_week()

        # Проверяем, что получаем только одного робота
        self.assertEqual(robots[0]['model'], self.robot_data['model'])
        self.assertEqual(robots[0]['version'], self.robot_data['version'])
        self.assertEqual(robots[0]['count'], 2)

    def test_prepare_empty_excel_workbook(self):
        """Тест функции, подготваливающей пустой Excel Workbook."""
        workbook = prepare_empty_excel_workbook()
        self.assertEqual(len(workbook.sheetnames), 0)

    def test_prepare_robot_data_before_writing(self):
        """
        Тест функции, подготваливающей данные роботов к записи в Excel таблице.
        """
        grouped_robots = [
            {'model': 'R2', 'version': 'D2', 'count': 2},
            {'model': 'R2', 'version': 'D2', 'count': 1},
            {'model': 'X5', 'version': 'L5', 'count': 3}
        ]

        robot_data = prepare_robot_data_before_writing(grouped_robots)

        self.assertEqual(len(robot_data), 2)
        self.assertIn('R2', robot_data)
        self.assertIn('X5', robot_data)
        self.assertEqual(len(robot_data['R2']), 2)
        self.assertEqual(len(robot_data['X5']), 1)
