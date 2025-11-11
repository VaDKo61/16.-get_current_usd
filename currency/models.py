from django.db import models
from django.utils.timezone import now


class ExchangeRate(models.Model):
    """
    Модель для хранения курса USD к RUB.

    Поля:
        rate (Decimal): Значение курса на момент запроса.
        timestamp (DateTime): Время получения курса.
    """
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Курс USD к RUB'
    )
    timestamp = models.DateTimeField(default=now, verbose_name='Время получения курса')

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта: курс доллара в рублях.
        """
        return f'{self.rate} RUB'

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'
