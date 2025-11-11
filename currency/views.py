from datetime import timedelta

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils.timezone import now
from django.shortcuts import redirect
from django.db import transaction

from .models import ExchangeRate
from .services import fetch_usd_rate, format_timestamp

DELAY = timedelta(seconds=10)


def get_current_usd(request: HttpRequest) -> JsonResponse:
    """
    Возвращает JSON с текущим курсом USD к RUB и 10 последними запросами.
    """
    latest_query = ExchangeRate.objects.order_by('-timestamp').first()

    if not latest_query or (now() - latest_query.timestamp > DELAY):
        try:
            with transaction.atomic():
                latest_query = ExchangeRate.objects.order_by('-timestamp').first()
                if not latest_query or (now() - latest_query.timestamp > DELAY):
                    rate = fetch_usd_rate()
                    ExchangeRate.objects.create(rate=rate)
        except Exception as e:
            return JsonResponse(
                {'error': 'Ошибка при получении курса', 'details': str(e)},
                status=500
            )

    last_rates = list(
        ExchangeRate.objects
        .only('rate', 'timestamp')
        .order_by('-timestamp')[:10]
        .values('rate', 'timestamp')
    )

    return JsonResponse({
        'current_rate': float(last_rates[0]['rate']),
        'last_10_rates': [
            {'timestamp': format_timestamp(r['timestamp']), 'rate': float(r['rate'])}
            for r in last_rates
        ]
    })


def redirect_to_usd(request: HttpRequest) -> HttpResponse:
    """
    Редирект с главной страницы на /get-current-usd/.
    """

    return redirect('get_current_usd')
