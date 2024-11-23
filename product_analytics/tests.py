from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, SalesRecord, ProductEngagement


class ProductPerformanceAnalyticsTests(APITestCase):
    def setUp(self):
        # Create dummy products
        product1 = Product.objects.create(
            name="Product 1", description="Description 1", cost_price=50.00, selling_price=100.00
        )
        product2 = Product.objects.create(
            name="Product 2", description="Description 2", cost_price=30.00, selling_price=60.00
        )

        # Create dummy sales records
        SalesRecord.objects.create(product=product1, quantity=10)
        SalesRecord.objects.create(product=product2, quantity=20)

    def test_top_selling_products(self):
        url = reverse("top-selling")  # Updated to match urlpatterns
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_record_engagement(self):
        url = reverse("engagement")  # Updated to match urlpatterns
        data = {"product_id": str(Product.objects.first().id), "engagement_type": "view"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_profit_margin(self):
        url = reverse("profit-margin")  # Updated to match urlpatterns
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
