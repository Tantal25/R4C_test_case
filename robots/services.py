import io

from django.db.models import Count
from django.utils import timezone
from openpyxl import Workbook

from .models import Robot


def db_robot_creation(data):
    """
    Функция создающая в базе данных запись о произведенном роботе
    на основе полученных данных. Возвращает результирующее сообщение.
    """

    Robot.objects.create(
        model=data['model'],
        version=data['version'],
        created=data['created'],
        serial=f"{data['model']}-{data['version']}"
        )

    return {
        'Результат': 'Данные о производстве робота приняты',
        'model': data['model'],
        'version': data['version']
        }


def get_robots_created_for_week():
    """
    Функция получающая из базы данных выборку произведенных за неделю роботов.
    """

    # Устанавливаем ограничение по времени для отчета
    last_week = timezone.now() - timezone.timedelta(weeks=1)

    # Получаем из базы всех роботов произведенных за неделю
    robots = Robot.objects.filter(created__gte=last_week)

    # Возвращаем выборку по моделям
    return robots.values('model', 'version').annotate(count=Count('model'))


def prepare_empty_excel_workbook():
    """Функция подготавливающая пустой Excel workbook."""

    workbook = Workbook()
    sheet = workbook.active
    workbook.remove(sheet)  # Убираем дефолтную пустую страницу
    return workbook


def prepare_robot_data_before_writing(grouped_robots):
    """
    Функция собирает в словарь данные по роботам из сгрупированной выборки.
    """

    robot_dict = {}  # подготавливаем словарь для отчета

    # наполняем словарь моделями и разными их версиями с количеством
    for group in grouped_robots:
        if group['model'] not in robot_dict:
            robot_dict[group['model']] = []
        robot_dict[group['model']].append((group['version'], group['count']))

    return robot_dict


def writing_robots_data_in_excel_file(robots_data, workbook):
    """
    Функция записывает в Excel Workbook данные из переданого словаря.
    """

    for model, versions in robots_data.items():
        # Для каждой модели создаем страницу
        sheet = workbook.create_sheet(title=model)
        # Делаем на каждой странице заголовки столбцов
        sheet.append(['Модель', 'Версия', 'Количество за неделю'])

        # На каждой странице выводим разбивку по версия и количеству
        for version, count in versions:
            sheet.append([model, version, count])


def prepare_excel_file_for_sending(workbook):
    """
    Функция подготавливает Excel файл для отправки.
    """

    excel_file = io.BytesIO()
    workbook.save(excel_file)  # переводим наши данные в Excel файл
    excel_file.seek(0)  # Перемещаем указатель файла в начало файла
    return excel_file
