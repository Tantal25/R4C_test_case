import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from .models import Robot
from .forms import JsonForm, RobotForm


def json_robot_creation(request):
    """Вью функция создающая робота в базе данных через шаблон c JSON."""
    form = JsonForm(request.POST or None)
    if request.method == 'POST':
        form2 = RobotForm(json.loads(request.POST['json_data']))
        result_message = ''
        if form2.is_valid():
            data = form2.cleaned_data

            Robot.objects.create(
                serial=f"{data['model']}-{data['version']}",
                model=data.get('model'),
                version=data.get('version'),
                created=data.get('created')
            )

            result_message = (
                f'Данные о производстве робота модели {data['model']} '
                f'версии {data['version']} приняты'
            )

        if result_message:
            final_dict = {'result_message': result_message}
        else:
            final_dict = {'form': form2}

        return render(request, 'json_robot_creation.html', final_dict)

    return render(request, 'json_robot_creation.html', {'form': form})


@csrf_exempt
@require_http_methods(('POST',))
def robot_creation_API(request):
    """"Вью для эндпоинта, создающая робота в базе данных через запрос."""
    try:
        form = RobotForm(json.loads(request.body))
        if form.is_valid():
            data = form.cleaned_data

            Robot.objects.create(
                model=data['model'],
                version=data['version'],
                created=data['created'],
                serial=f"{data['model']}-{data['version']}"
            )

            return JsonResponse({
                'Cообщение': 'Данные о производстве робота приняты',
                'model': data['model'],
                'version': data['version']
            })
        return JsonResponse({'error': form.errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неправильный формат JSON'}, status=400)
