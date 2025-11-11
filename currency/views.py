import requests
from datetime import timedelta
from decimal import Decimal

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils.timezone import now
from django.shortcuts import redirect

from .models import ExchangeRate

OPEN_ER_API_URL = 'https://open.er-api.com/v6/latest/USD'
DELAY = timedelta(seconds=10)


def fetch_usd_rate() -> Decimal:
    """
    Запрос текущего курса USD к RUB по API (open.er-api.com)

    :return: Курс доллара к рублю.
    :raises: ValueError, requests.RequestException
    """
    response = requests.get(OPEN_ER_API_URL)
    response.raise_for_status()
    data = response.json()

    if data['result'] != 'success':
        raise ValueError('API returned unsuccessful result')

    rub_rate = data['rates'].get('RUB')
    if rub_rate is None:
        raise ValueError("RUB rate not found in API response")

    return Decimal(str(rub_rate))


def get_current_usd(request: HttpRequest) -> JsonResponse:
    """
    Возвращает JSON с текущим курсом USD к RUB и 10 последних запросов.

    :return: JSON-ответ.
    """
    latest_query = ExchangeRate.objects.order_by('-timestamp').first()

    if not latest_query or now() - latest_query.timestamp > DELAY:
        try:
            rate = fetch_usd_rate()
            ExchangeRate.objects.create(rate=rate)
        except Exception as e:
            return JsonResponse({'error': 'Ошибка при получении курса', 'details': str(e)},
                                status=500)

    latest_rate = ExchangeRate.objects.order_by('-timestamp').first()
    last_10 = ExchangeRate.objects.order_by('-timestamp')[:10]

    return JsonResponse({
        'current_rate': float(latest_rate.rate),
        'last_10_rates': [
            {'rate': float(r.rate), 'timestamp': r.timestamp.isoformat()} for r in last_10
        ]
    })


def redirect_to_usd(request: HttpRequest) -> HttpResponse:
    """
    Редирект с главной страницы на /get-current-usd/.
    """
    return redirect('get_current_usd')
