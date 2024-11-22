from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Sale
from .services import SalesPerformanceService
from .api.v1.serializers import SalesPerformanceSerializer

# Create your tests here.


class SalesAnalyticsTests(TestCase):
    def setUp(self):
        # Create test data
        self.now = timezone.now()
        self.products = ["solar_panels", "wind_turbines", "batteries"]
        self.prices = {"solar_panels": 1000, "wind_turbines": 2000, "batteries": 500}

        # Create sales for the last 90 days
        for i in range(90):
            date = self.now - timedelta(days=i)
            for product in self.products:
                Sale.objects.create(
                    product=product,
                    quantity=i % 5 + 1,  # Varying quantities 1-5
                    price=self.prices[product],
                    created_at=date,
                )

    def test_get_revenue_trends(self):
        service = SalesPerformanceService()
        trends = service.get_revenue_trends()

        # Test structure
        self.assertIn("daily", trends)
        self.assertIn("weekly", trends)
        self.assertIn("monthly", trends)
        self.assertIn("quarterly", trends)

        # Test daily revenues
        daily_revenues = trends["daily"]
        self.assertTrue(len(daily_revenues) > 0)
        self.assertIn("day", daily_revenues[0])
        self.assertIn("revenue", daily_revenues[0])

        # Test revenue calculations
        first_day = daily_revenues[0]
        self.assertIsInstance(first_day["revenue"], (int, float, Decimal))
        self.assertTrue(first_day["revenue"] >= 0)

    def test_get_sales_by_product(self):
        service = SalesPerformanceService()
        sales = service.get_sales_by_product()

        # Test all products are present
        for product in self.products:
            self.assertIn(product, sales)

        # Test sales values
        for product, amount in sales.items():
            self.assertIsInstance(amount, (int, float, Decimal))
            self.assertTrue(amount >= 0)

        # Verify relative amounts (wind turbines should have highest revenue due to price)
        self.assertTrue(sales["wind_turbines"] > sales["solar_panels"])
        self.assertTrue(sales["solar_panels"] > sales["batteries"])

    def test_serializer_success(self):
        service = SalesPerformanceService()
        data = {
            "revenue_trends": service.get_revenue_trends(),
            "sales_by_product": service.get_sales_by_product(),
        }

        serializer = SalesPerformanceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        # Test status and message
        self.assertEqual(serialized_data["status"], "success")
        self.assertEqual(serialized_data["message"], "Data retrieved successfully")

        # Test data structure
        self.assertIn("revenue_trends", serialized_data)
        self.assertIn("sales_by_product", serialized_data)

    def test_serializer_with_empty_data(self):
        # Test with empty data
        data = {
            "revenue_trends": {},
            "sales_by_product": {},
        }

        serializer = SalesPerformanceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        # Even with empty data, status should be success
        self.assertEqual(serialized_data["status"], "success")

    def tearDown(self):
        # Clean up test data
        Sale.objects.all().delete()
