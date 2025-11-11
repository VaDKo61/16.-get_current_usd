from django.test import TestCase, Client
from unittest.mock import patch
from decimal import Decimal

from currency.models import ExchangeRate


class GetCurrentUsdViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_existing_rate(self):
        """Проверяет на возврат курса"""
        ExchangeRate.objects.create(rate=Decimal('81.1234'))

        response = self.client.get('/get-current-usd/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('current_rate', data)
        self.assertTrue(len(data['last_10_rates']) >= 1)

    @patch('currency.views.fetch_usd_rate', side_effect=Exception('API error'))
    def test_handles_fetch_error(self, mock_fetch):
        """Если fetch_usd_rate падает — возвращается 500 и JSON с ошибкой."""
        response = self.client.get('/get-current-usd/')
        self.assertEqual(response.status_code, 500)

        data = response.json()
        self.assertIn('error', data)
        self.assertIn('Ошибка при получении курса', data['error'])

    def test_returns_10_latest_rates(self):
        """Возвращает не более 10 последних записей."""
        for i in range(15):
            ExchangeRate.objects.create(rate=Decimal(f'80.{i:04d}'))

        response = self.client.get('/get-current-usd/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['last_10_rates']), 10)

        self.assertGreaterEqual(
            data['last_10_rates'][0]['rate'],
            data['last_10_rates'][-1]['rate']
        )
