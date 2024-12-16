from .models import Order


def find_unprocessed_order(robot_serial):
    """Функция которая ищет заказы по серийному номеру заказы на робота."""

    return Order.objects.filter(
            robot_serial=robot_serial, in_process=False).first()


def change_order_in_process_status(order):
    """Функция которая меняет статус заказа на True."""

    order.in_process = True
    order.save()


def db_order_creation(data, customer):
    """
    Функция которая создает запись заказа в БД на основе
    серийного номера и данных пользователя сделавшего заказ.
    """
    Order.objects.create(customer=customer, robot_serial=data['robot_serial'])
