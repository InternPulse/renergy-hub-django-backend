from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
import unittest
from datetime import datetime, timedelta

class FinancialAnalyticsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_list_endpoint(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        response = self.client.get('/api/v1/financial/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        
        product_data = response.data['results'][0]
        self.assertEqual(product_data['product_id'], 1)
        self.assertEqual(product_data['total_revenue'], 800000)
        self.assertEqual(product_data['total_cost'], 560000)
        self.assertEqual(product_data['total_quantity_sold'], 10)
        self.assertEqual(product_data['total_profit'], 240000)
        self.assertEqual(product_data['average_stock'], 10)
        self.assertAlmostEqual(product_data['profit_margin'], 30, places=2)
        self.assertEqual(product_data['average_price'], 80000)
        self.assertEqual(product_data['stock_turnover_rate'], 1)
        self.assertTrue(product_data['is_profitable'])
        self.assertEqual(product_data['profit_per_unit'], 24000)
        
    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_filter_by_date_range(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/financial/analytics/?start_date={start_date}&end_date={end_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_filter_by_month(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        response = self.client.get('/api/v1/financial/analytics/?month=12')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_invalid_month(self):
        response = self.client.get('/api/v1/financial/analytics/?month=13')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_filter_by_day(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        response = self.client.get('/api/v1/financial/analytics/?day=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_invalid_day(self):
        response = self.client.get('/api/v1/financial/analytics/?day=32')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_filter_by_year(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        current_year = datetime.now().year
        response = self.client.get(f'/api/v1/financial/analytics/?year={current_year}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_analytics_calculations(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            },
            {
                "id": 2,
                "categoryId": 1,
                "userId": 1,
                "name": "Solar Panel",
                "description": "A solar panel",
                "price": "100000",
                "stock": 5,
                "image": "https://example.com/solar-panel.jpg",
                "createdAt": "2024-12-04T10:15:30.123Z",
                "updatedAt": "2024-12-04T10:15:30.123Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        response = self.client.get('/api/v1/financial/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
        
        inverter_data = next(item for item in response.data['results'] if item['name'] == 'Inverter')
        solar_panel_data = next(item for item in response.data['results'] if item['name'] == 'Solar Panel')
        
        # Test Inverter calculations
        self.assertEqual(inverter_data['total_revenue'], 800000)
        self.assertEqual(inverter_data['total_cost'], 560000)
        self.assertEqual(inverter_data['total_quantity_sold'], 10)
        self.assertEqual(inverter_data['total_profit'], 240000)
        self.assertEqual(inverter_data['average_stock'], 10)
        self.assertAlmostEqual(inverter_data['profit_margin'], 30, places=2)
        self.assertEqual(inverter_data['average_price'], 80000)
        self.assertEqual(inverter_data['stock_turnover_rate'], 1)
        self.assertTrue(inverter_data['is_profitable'])
        self.assertEqual(inverter_data['profit_per_unit'], 24000)
        
        # Test Solar Panel calculations
        self.assertEqual(solar_panel_data['total_revenue'], 500000)
        self.assertEqual(solar_panel_data['total_cost'], 350000)
        self.assertEqual(solar_panel_data['total_quantity_sold'], 5)
        self.assertEqual(solar_panel_data['total_profit'], 150000)
        self.assertEqual(solar_panel_data['average_stock'], 5)
        self.assertAlmostEqual(solar_panel_data['profit_margin'], 30, places=2)
        self.assertEqual(solar_panel_data['average_price'], 100000)
        self.assertEqual(solar_panel_data['stock_turnover_rate'], 1)
        self.assertTrue(solar_panel_data['is_profitable'])
        self.assertEqual(solar_panel_data['profit_per_unit'], 30000)

    @patch('financial_analytics.api_client.ProductManagementAPI.get_products')
    def test_filter_by_min_profit(self, mock_get_products):
        mock_get_products.return_value = [
            {
                "id": 1,
                "categoryId": 1,
                "userId": 1,
                "name": "Inverter",
                "description": "A battery",
                "price": "80000",
                "stock": 10,
                "image": "https://example.com/inverter.jpg",
                "createdAt": "2024-12-03T15:28:50.865Z",
                "updatedAt": "2024-12-03T15:28:50.865Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            },
            {
                "id": 2,
                "categoryId": 1,
                "userId": 1,
                "name": "Solar Panel",
                "description": "A solar panel",
                "price": "100000",
                "stock": 5,
                "image": "https://example.com/solar-panel.jpg",
                "createdAt": "2024-12-04T10:15:30.123Z",
                "updatedAt": "2024-12-04T10:15:30.123Z",
                "category": {
                    "id": 1,
                    "categoryName": "Plumbing",
                    "description": "Plumbeer"
                }
            }
        ]

        response = self.client.get('/api/v1/financial/analytics/?min_profit=200000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Inverter')

if __name__ == '__main__':
    unittest.main()

