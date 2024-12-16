from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .forms import OrderForm

from customers.models import Customer
from .services import db_order_creation


def create_order(request):
    """
    Вью функция создающая заказ на робота в базе данных на
    основе серийного номера и почты пользователя.
    """

    form = OrderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            # Пробуем найти пользователя с вводимым заказом
            customer = Customer.objects.get(email=data['email'])

            # Создаем заказ в базе данных
            db_order_creation(data, customer)

            return render(
                request,
                'orders/create_order.html',
                {'result_message':
                 f'Заказ на робота {data['robot_serial']} принят.'}
                 )

        else:
            # Если форма не валидна, возвращаем причину сбоя в форме
            return HttpResponseBadRequest(
                render(request, 'orders/create_order.html', {'form': form})
                )

    # Рендерим форму для ввода при GET запросе
    return render(request, 'orders/create_order.html', {'form': form})
