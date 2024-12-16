from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .forms import CustomerForm


def create_customer(request):
    """
    Вью функция создающая заказ на робота в базе данных на
    основе серийного номера и почты пользователя.
    """

    form = CustomerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return render(
                request,
                'create_customer.html',
                {'result_message': 'Регистрация прошла успешно.'}
                )

        # Если форма не валидна, возвращаем ошибку
        return HttpResponseBadRequest(render(
            request,
            'create_customer.html',
            {'form': form})
            )

    # Рендерим форму для ввода при GET запросе
    return render(request, 'create_customer.html', {'form': form})
