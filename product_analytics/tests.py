from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, SalesRecord, ProductEngagement
import uuid


class ProductViewsTestCase(TestCase):
    def setUp(self):
        # Set up a client for making API requests
        self.client = APIClient()

        # Create test product data
        self.product1 = Product.objects.create(
            name="Product 1",
            description="Test Product 1",
            cost_price=10.00,
            selling_price=20.00
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            description="Test Product 2",
            cost_price=15.00,
            selling_price=30.00
        )

        # Create test sales data (Mocking sales for top-selling products)
        SalesRecord.objects.create(product=self.product1, quantity=50)
        SalesRecord.objects.create(product=self.product2, quantity=30)

        # URL for the views to be tested
        self.top_selling_url = reverse('products:top-selling')
        self.product_engagement_url = reverse('products:engagement')
        self.profit_margin_url = reverse('products:profit-margin')

    def test_top_selling_products_get(self):
        # Test GET request to TopSellingProductsView
        response = self.client.get(self.top_selling_url)

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the correct product data
        products = response.data['results']
        self.assertGreater(len(products), 0, "There should be at least one top-selling product.")

        # Check that the top-selling product is correctly sorted by quantity sold
        self.assertEqual(products[0]['name'], self.product1.name)

    def test_product_engagement_post(self):
        # Test POST request to ProductEngagementView (for creating engagement)
        data = {
            'product_id': str(self.product1.id),
            'engagement_type': 'view'
        }
        response = self.client.post(self.product_engagement_url, data, format='json')

        # Ensure status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check response message
        self.assertEqual(response.data['message'], 'Engagement recorded successfully.')

        # Ensure engagement is created in the database
        self.assertEqual(ProductEngagement.objects.count(), 1)

    def test_product_engagement_post_missing_data(self):
        # Test POST request to ProductEngagementView (missing product_id)
        data = {'engagement_type': 'view'}
        response = self.client.post(self.product_engagement_url, data, format='json')

        # Ensure status code is 400 Bad Request due to missing required data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check error message
        self.assertEqual(response.data['error'], 'Product ID and Engagement Type are required.')

    def test_product_engagement_get(self):
        # Create engagement data for testing GET
        ProductEngagement.objects.create(product=self.product1, engagement_type='view')
        ProductEngagement.objects.create(product=self.product2, engagement_type='click')

        # Test GET request to ProductEngagementView
        response = self.client.get(self.product_engagement_url)

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that response contains correct engagement data
        engagement_data = response.data['results']
        self.assertGreater(len(engagement_data), 0, "There should be at least one engagement record.")

    def test_profit_margin_get(self):
        # Test GET request to ProfitMarginView
        response = self.client.get(self.profit_margin_url)

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the profit margins for the products
        profit_margins = response.data['results']
        self.assertGreater(len(profit_margins), 0, "There should be at least one product with a profit margin.")

        # Check that the profit margin is calculated correctly
        for product_data in profit_margins:
            profit_margin = product_data['profit_margin']
            product = Product.objects.get(name=product_data['product_name'])
            expected_profit_margin = round((product.selling_price - product.cost_price) / product.selling_price * 100,
                                           2)
            self.assertEqual(profit_margin, expected_profit_margin)

    def test_product_not_found(self):
        # Test POST request to ProductEngagementView with a non-existing product ID
        data = {
            'product_id': str(uuid.uuid4()),  # Non-existing product ID
            'engagement_type': 'click'
        }
        response = self.client.post(self.product_engagement_url, data, format='json')

        # Ensure status code is 404 Not Found for invalid product
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Product not found.')

    def test_invalid_engagement_type(self):
        # Test POST request to ProductEngagementView with an invalid engagement type
        data = {
            'product_id': str(self.product1.id),
            'engagement_type': 'invalid'  # Invalid engagement type
        }
        response = self.client.post(self.product_engagement_url, data, format='json')

        # Ensure status code is 400 Bad Request for invalid engagement type
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid engagement type. Accepted values: "view", "click".')

