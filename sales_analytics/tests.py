from django.test import TestCase
from unittest.mock import patch, MagicMock
from datetime import datetime, date
import pytz
import requests
from .services import SalesPerformanceService
from .api_client import ProductManagementAPI

class TestSalesPerformanceService(TestCase):
    def setUp(self):
        self.service = SalesPerformanceService()
        self.mock_products = [
            {"id": 1, "name": "Product A", "stock": 10, "price": "100.00", "createdAt": "2023-01-15T10:00:00Z"},
            {"id": 2, "name": "Product B", "stock": 5, "price": "50.00", "createdAt": "2023-02-20T14:30:00Z"},
            {"id": 3, "name": "Product A", "stock": 8, "price": "100.00", "createdAt": "2023-03-10T09:15:00Z"},
        ]

    @patch.object(ProductManagementAPI, 'get_products')
    def test_get_revenue_trends(self, mock_get_products):
        mock_get_products.return_value = self.mock_products
        trends = self.service.get_revenue_trends()

        self.assertIn('daily', trends)
        self.assertIn('weekly', trends)
        self.assertIn('monthly', trends)
        self.assertIn('quarterly', trends)

        # Check daily revenue
        self.assertEqual(trends['daily']['2023-01-15'], 1000.0)
        self.assertEqual(trends['daily']['2023-02-20'], 250.0)
        self.assertEqual(trends['daily']['2023-03-10'], 800.0)

        # Check monthly revenue
        self.assertEqual(trends['monthly'][1], 1000.0)
        self.assertEqual(trends['monthly'][2], 250.0)
        self.assertEqual(trends['monthly'][3], 800.0)

    @patch.object(ProductManagementAPI, 'get_products')
    def test_get_revenue_trends_error_handling(self, mock_get_products):
        mock_get_products.side_effect = Exception("API Error")
        
        with self.assertRaises(RuntimeError):
            self.service.get_revenue_trends()
            
            
    def test_parse_date(self):
        # Test UTC date
        utc_date = self.service.parse_date("2023-01-15T10:00:00Z")
        self.assertEqual(utc_date, datetime(2023, 1, 15, 10, 0, tzinfo=pytz.UTC))

        # Test non-UTC date (now assumed to be UTC)
        non_utc_date = self.service.parse_date("2023-02-20T14:30:00")
        self.assertEqual(non_utc_date, datetime(2023, 2, 20, 14, 30, tzinfo=pytz.UTC))

        # Test date with microseconds
        micro_date = self.service.parse_date("2023-03-25T08:45:30.123456")
        self.assertEqual(micro_date, datetime(2023, 3, 25, 8, 45, 30, 123456, tzinfo=pytz.UTC))

        # Test invalid date
        with self.assertRaises(ValueError):
            self.service.parse_date("invalid-date")
            
    @patch.object(ProductManagementAPI, 'get_products')
    def test_get_sales_by_product(self, mock_get_products):
        mock_get_products.return_value = self.mock_products
        sales = self.service.get_sales_by_product()

        self.assertEqual(sales['Product A'], 1800.0)
        self.assertEqual(sales['Product B'], 250.0)

    @patch.object(ProductManagementAPI, 'get_products')
    def test_get_sales_by_time_of_year(self, mock_get_products):
        mock_get_products.return_value = self.mock_products
        sales = self.service.get_sales_by_time_of_year()

        self.assertEqual(sales[1], 1000.0)
        self.assertEqual(sales[2], 250.0)
        self.assertEqual(sales[3], 800.0)

    @patch.object(ProductManagementAPI, 'get_products')
    def test_error_handling_in_revenue_calculation(self, mock_get_products):
        # Test with a product missing required fields
        invalid_product = {"id": 4, "name": "Invalid Product", "stock": "invalid", "price": "not a number"}
        mock_get_products.return_value = self.mock_products + [invalid_product]

        # This should not raise an exception, but log an error
        trends = self.service.get_revenue_trends()

        # Check that valid products are still processed
        self.assertEqual(trends['daily']['2023-01-15'], 1000.0)
        self.assertEqual(trends['daily']['2023-02-20'], 250.0)
        self.assertEqual(trends['daily']['2023-03-10'], 800.0)

class TestProductManagementAPI(TestCase):
    def setUp(self):
        self.api = ProductManagementAPI()

    @patch('requests.get')
    def test_get_products(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': [{'id': 1, 'name': 'Test Product'}]}
        mock_get.return_value = mock_response

        products = self.api.get_products()

        self.assertEqual(products, [{'id': 1, 'name': 'Test Product'}])
        mock_get.assert_called_once_with(f"{self.api.base_url}/products")

    @patch('requests.get')
    def test_get_products_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        with self.assertRaises(requests.exceptions.RequestException):
            self.api.get_products()