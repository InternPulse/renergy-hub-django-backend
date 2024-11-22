from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .viewsets import FinancialAnalyticsViewSet
from datetime import datetime, timedelta

class FinancialAnalyticsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.viewset = FinancialAnalyticsViewSet()

    def test_list_endpoint(self):
        response = self.client.get('/api/v1/financial/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)

    def test_top_products_endpoint(self):
        response = self.client.get('/api/v1/financial/analytics/top_products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('top_products', response.data)
        self.assertLessEqual(len(response.data['top_products']), 5)

    def test_selling_at_loss_endpoint(self):
        response = self.client.get('/api/v1/financial/analytics/selling_at_loss/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('loss_products', response.data)

    def test_profit_records_endpoint(self):
        response = self.client.get('/api/v1/financial/analytics/profit_records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profit_products', response.data)

    def test_filter_by_date_range(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/financial/analytics/?start_date={start_date}&end_date={end_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_month(self):
        response = self.client.get('/api/v1/financial/analytics/?month=6')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_invalid_month(self):
        response = self.client.get('/api/v1/financial/analytics/?month=13')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_day(self):
        response = self.client.get('/api/v1/financial/analytics/?day=15')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_invalid_day(self):
        response = self.client.get('/api/v1/financial/analytics/?day=32')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_year(self):
        current_year = datetime.now().year
        response = self.client.get(f'/api/v1/financial/analytics/?year={current_year}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
