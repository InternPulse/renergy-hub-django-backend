import unittest
from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import requests
from .views import TopSellingProductsView
from .api_client import ProductManagementAPI
from .serializers import ResponseSerializer, ProductSerializer

class TopSellingProductsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('top-selling')
        self.patcher = patch.object(ProductManagementAPI, 'get_products')
        self.mock_get_products = self.patcher.start()
        self.mock_products = [
            {'name': 'Product A', 'price': 10},
            {'name': 'Product B', 'price': 20},
            {'name': 'Product A', 'price': 10},
            {'name': 'Product C', 'price': 30},
            {'name': 'Product B', 'price': 20},
        ]
        self.mock_get_products.return_value = self.mock_products

    def tearDown(self):
        self.patcher.stop()

    # ... (rest of the test methods remain the same)

class ProductManagementAPITestCase(TestCase):
    def setUp(self):
        self.api_client = ProductManagementAPI()

    @patch('requests.get')
    def test_get_products_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'data': [{'name': 'Test Product', 'price': 10}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        products = self.api_client.get_products()

        self.assertEqual(products, [{'name': 'Test Product', 'price': 10}])
        mock_get.assert_called_once_with(f"{self.api_client.base_url}/products")

    @patch('requests.get')
    def test_get_products_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.api_client.get_products()

    @patch('requests.get')
    def test_get_products_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.api_client.get_products()

if __name__ == '__main__':
    unittest.main()