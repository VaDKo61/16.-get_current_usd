from decimal import Decimal

import requests

OPEN_ER_API_URL = 'https://open.er-api.com/v6/latest/USD'


def fetch_usd_rate() -> Decimal:
    """
    Возвращает текущий курс USD к RUB с API open.er-api.com.

    :return: Курс доллара к рублю.
    :raises ValueError: если ответ неуспешен или данные некорректны.
    :raises requests.RequestException: при сетевых ошибках.
    """

    try:
        response = requests.get(OPEN_ER_API_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise requests.RequestException(f'Ошибка при запросе API: {exc}')

    data = response.json()
    if data.get('result') != 'success':
        raise ValueError(f'API вернул ошибку: {data.get('error-type', 'unknown')}')

    try:
        rub_rate = Decimal(str(data['rates']['RUB']))
    except (KeyError, TypeError, ValueError):
        raise ValueError('Некорректные данные в ответе API')

    return rub_rate


def format_timestamp(dt):
    """
    Возвращает дату в удобном формате, например: '11 ноября 2025, 10:52'
    """
    return dt.strftime('%d.%m.%Y %H:%M:%S')
