from django.db.models import Sum, F
from django.db import models
from datetime import datetime
from .api_client import ProductManagementAPI


class SalesPerformanceService:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_api = ProductManagementAPI()

    def get_revenue_trends(self):
        products = self.product_api.get_products()

        # Group products by time period and calculate revenue
        def group_by_time_period(period_func):
            grouped_data = {}
            for product in products:
                created_at = self.parse_date(product["createdAt"])
                time_period = period_func(created_at)

                # Convert stock and price to appropriate numeric types
                stock = int(product["stock"])
                price = float(product["price"])

                grouped_data[time_period] = grouped_data.get(time_period, 0) + (stock * price)
            return grouped_data

        # Convert the time period keys to strings for JSON serialization
        def convert_keys_to_strings(data):
            return {str(key): value for key, value in data.items()}

        daily_revenue = group_by_time_period(lambda x: x.date())
        weekly_revenue = group_by_time_period(lambda x: x.isocalendar()[1])
        monthly_revenue = group_by_time_period(lambda x: x.month)
        quarterly_revenue = group_by_time_period(
            lambda x: (x.year, (x.month - 1) // 3 + 1)
        )

        return {
            "daily": convert_keys_to_strings(daily_revenue),
            "weekly": weekly_revenue,  # Keys are already JSON-serializable
            "monthly": monthly_revenue,  # Keys are integers
            "quarterly": convert_keys_to_strings(quarterly_revenue),  # Convert tuples to strings
        }

    def parse_date(self, date_string):
        """Parse the date string into a datetime object."""
        try:
            return datetime.fromisoformat(date_string)  # Assumes ISO 8601 format
        except ValueError:
            raise ValueError(f"Invalid date format: {date_string}")

    def get_sales_by_product(self):
        products = self.product_api.get_products()

        sales_by_product = {}
        for product in products:
            name = product["name"]  # Replace with actual field name

            # Convert stock and price to appropriate numeric types
            stock = int(product["stock"])  # Ensure stock is an integer
            price = float(product["price"])  # Ensure price is a float

            sales_by_product[name] = sales_by_product.get(name, 0) + (stock * price)

        return sales_by_product

    def get_sales_by_time_of_year(self):
        products = self.product_api.get_products()

        sales_by_month = {}
        for product in products:
            created_at = self.parse_date(product["createdAt"])

            # Convert stock and price to appropriate numeric types
            stock = int(product["stock"])  # Ensure stock is an integer
            price = float(product["price"])  # Ensure price is a float

            month = created_at.month
            sales_by_month[month] = sales_by_month.get(month, 0) + (stock * price)

        return sales_by_month
