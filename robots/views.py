import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .validation import validate_model
from .models import Robot
from .forms import RobotForm


def robot_creation_through_fields(request):
    """Вью функция создающая робота в базе данных через шаблон с полями."""
    form = RobotForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'fields_robot_creation.html', {'form': form})


def robot_creation_through_json(request):
    """Вью функция создающая робота в базе данных через шаблон c JSON."""
    try:
        request_data = json.loads(request.POST.get('json_data'))

        validate_model(request_data['model'])
        Robot.objects.create(**request_data)

        return JsonResponse({
                'Cообщение': 'Данные о производстве робота приняты',
                'model': request_data['model'],
                'version': request_data['version']
            })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неправильный формат JSON'}, status=400)


@csrf_exempt
@require_http_methods(('POST',))
def robot_creation_without_csrf(request):
    """"Вью для эндпоинта, создающая робота в базе данных через запрос."""
    try:
        request_data = json.loads(request.body)

        # Проверяем есть ли модель в списке разрешенных
        validate_model(request_data['model'])

        Robot.objects.create(**request_data)

        return JsonResponse({
            'Cообщение': 'Данные о производстве робота приняты',
            'model': request_data['model'],
            'version': request_data['version']
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неправильный формат JSON'}, status=400)
