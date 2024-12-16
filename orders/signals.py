from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver

from robots.models import Robot
from .services import change_order_in_process_status, find_unprocessed_order


@receiver(post_save, sender=Robot)
def send_email_order_ready(sender, instance, created, **kwargs):
    """
    Сигнал, который при создании робота, проверяет нет ли заказов
    на робота с указанным серийным номером и если такой заказ есть
    переводит заказ в обработку.
    """

    if created:
        # Получаем заказ с соответствовующим серийному номеру
        # робота и заказ ещё не был обработан
        order = find_unprocessed_order(instance.serial)

        # Если есть необработанный заказ на такого робота, то отправляем письмо
        if order:
            send_mail(
                subject='R4C - Robot Order',
                message=(
                    'Добрый день!\n'
                    'Недавно вы интересовались нашим роботом '
                    f'модели {instance.model}, версии {instance.version}.\n'
                    'Этот робот теперь в наличии. '
                    'Если вам подходит этот вариант'
                    ' - пожалуйста, свяжитесь с нами'
                    ),
                from_email='R4C@email.com',
                recipient_list=(order.customer.email,)
                )

            # Меняем статус заказа на обработанный и сохраняем в БД
            change_order_in_process_status(order)
