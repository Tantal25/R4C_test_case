from django.db import models


class Robot(models.Model):
    serial = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name='Серийный номер'
        )
    model = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        verbose_name='Модель'
    )
    version = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        verbose_name='Версия'
    )
    created = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name='Дата создания'
    )
