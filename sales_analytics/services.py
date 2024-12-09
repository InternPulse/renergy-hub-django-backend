from django.db.models import Sum, F
from django.db import models
from datetime import datetime
from .api_client import ProductManagementAPI
import pytz


class SalesPerformanceService:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_api = ProductManagementAPI()

    def get_revenue_trends(self):
        try:
            products = self.product_api.get_products()

            # Group products by time period and calculate revenue
            def group_by_time_period(period_func):
                grouped_data = {}
                for product in products:
                    try:
                        created_at = self.parse_date(product["createdAt"])
                        time_period = period_func(created_at)

                        # Convert stock and price to appropriate numeric types
                        stock = int(product["stock"])
                        price = float(product["price"])

                        grouped_data[time_period] = grouped_data.get(time_period, 0) + (stock * price)
                    except (ValueError, KeyError) as e:
                        # Log the error and continue with the next product
                        print(f"Error processing product: {product.get('id', 'Unknown')}. Error: {str(e)}")
                        continue
                return grouped_data
            
        except Exception as e:
        # Log the error and re-raise with a more informative message
            print(f"Error in get_revenue_trends: {str(e)}")
            raise RuntimeError("An error occurred while calculating revenue trends. Please check the logs for more details.")

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
        """Parse the date string into a timezone-aware datetime object."""
        try:
            # Remove the 'Z' and parse the string
            date_string = date_string.rstrip('Z')
            dt = datetime.fromisoformat(date_string)
            
            # If the original string ended with 'Z', it was in UTC
            if date_string.endswith('Z'):
                dt = dt.replace(tzinfo=pytz.UTC)
            else:
                # If no timezone info, assume it's UTC
                dt = pytz.UTC.localize(dt)
            
            return dt
        except ValueError:
            # If parsing fails, try a more lenient approach
            try:
                dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
                return pytz.UTC.localize(dt)
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
