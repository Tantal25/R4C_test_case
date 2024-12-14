import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import JsonForm, RobotForm
from .services import (
    db_robot_creation, get_robots_created_for_week,
    prepare_empty_excel_workbook, prepare_robot_data_before_writing,
    writing_robots_data_in_excel_file, prepare_excel_file_for_sending
    )


@csrf_exempt
@require_http_methods(('POST',))
def robot_creation_API(request):
    """"Вью для эндпоинта, создающая робота в базе данных через запрос."""
    try:
        # Передаем преобразованные из JSON данные в форму связанную с моделью
        form = RobotForm(json.loads(request.body))

        if form.is_valid():
            # Создаем робота и возвращаем результат создания
            return JsonResponse(db_robot_creation(form.cleaned_data))

        # Если форма не ваоидна, возвращаем возникшую ошибку
        return JsonResponse({'error': form.errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Некорректный формат, передайте данные в формате JSON.'},
            json_dumps_params={'ensure_ascii': False}, status=400
        )


def json_robot_creation(request):
    """
    Вью функция создающая робота в базе данных
    через передачу JSON в HTML темплейт.
    """
    # Форма для отрисовки в шаблоне при переданном GET запросе

    try:
        form = JsonForm()
        if request.method == 'POST':
            # Передаем преобразованные из JSON данные в форму связанную
            # с моделью, для валидации по полям модели.
            form2 = RobotForm(json.loads(request.POST['json_data']))

            if form2.is_valid():
                # Если форма валидна создаем робота и возвращаем результат
                result = {
                    'result_message': db_robot_creation(form2.cleaned_data)
                    }
            else:
                # Если форма не валидна, возвращаем причину сбоя
                result = {'form': form2}

            return render(request, 'json_robot_creation.html', result)

        # Рендерим форму для ввода при GET запросе
        return render(request, 'json_robot_creation.html', {'form': form})

    except json.JSONDecodeError:
        return HttpResponse(
            'Ошибка - некорректный формат данных. '
            'Передайте данные в формате JSON.', status=400
            )


@require_http_methods(('GET',))
def production_report(request):
    """
    Вью функция генерирующая отчет по произведенным роботам
    за неделю и отправляющая Excel файл.
    """
    # Получаем отсортированную выборку роботов произведенных за неделю
    grouped_robots = get_robots_created_for_week()

    if not grouped_robots:
        return HttpResponse(
            "В базе данных нет роботов произведенных за последнюю неделю",
            status=400
            )

    # Создаем наш пустой Excel workbook
    workbook = prepare_empty_excel_workbook()

    # Подготавливаем данные по роботам к записи
    robots_data = prepare_robot_data_before_writing(grouped_robots)

    # Заполняем отчет
    writing_robots_data_in_excel_file(robots_data, workbook)

    # Подготавливаем файл для отправки
    excel_file = prepare_excel_file_for_sending(workbook)

    response = HttpResponse(excel_file, content_type='application/ms-excel')
    response['Content-Disposition'] = (
        'attachment; filename=proudction_report.xlsx')
    return response
