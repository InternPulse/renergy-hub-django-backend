# from .models import Sale

# class SalesPerformanceService:
#     def get_revenue_trends(self):
#         # Query the database to get revenue data over time
#         # Return a dictionary with the revenue trends
#         return {
#             'daily': {...},
#             'weekly': {...},
#             'monthly': {...},
#             'quarterly': {...}
#         }

#     def get_sales_by_product(self):
#         # Query the database to get sales data for each product
#         # Return a dictionary with the sales by product
#         return {
#             'solar_panels': 50000,
#             'wind_turbines': 30000,
#             'batteries': 20000,
#         }



from django.db.models import Sum, F
from django.db import models
from .models import Sale
from datetime import datetime


class SalesPerformanceService:
    def get_revenue_trends(self):
            # Query the database to get revenue data over time
            daily_sales = Sale.objects.annotate(
                day=models.functions.TruncDate('created_at')
            ).values('day').annotate(
                revenue=Sum(F('quantity') * F('price'))
            ).order_by('day')
            
            weekly_sales = Sale.objects.annotate(
                week=models.functions.TruncWeek('created_at')
            ).values('week').annotate(
                revenue=Sum(F('quantity') * F('price'))
            ).order_by('week')
            
            monthly_sales = Sale.objects.annotate(
                month=models.functions.TruncMonth('created_at')
            ).values('month').annotate(
                revenue=Sum(F('quantity') * F('price'))
            ).order_by('month')
            
            quarterly_sales = Sale.objects.annotate(
                quarter=models.functions.TruncQuarter('created_at')
            ).values('quarter').annotate(
                revenue=Sum(F('quantity') * F('price'))
            ).order_by('quarter')

            return {
                'daily': list(daily_sales),
                'weekly': list(weekly_sales),
                'monthly': list(monthly_sales),
                'quarterly': list(quarterly_sales)
            }

    def get_sales_by_product(self):
        # Query the database to get sales data for each product
        sales_by_product = Sale.objects.values('product').annotate(
            total_sales=Sum(F('quantity') * F('price'))
        ).order_by('-total_sales')
        return {item['product']: item['total_sales'] for item in sales_by_product}

    # def get_sales_by_region(self):
    #     # Query the database to get sales data by region/location
    #     sales_by_region = Sale.objects.values('customer_region').annotate(
    #         total_sales=Sum(F('quantity') * F('price'))
    #     ).order_by('-total_sales')
    #     return {item['customer_region']: item['total_sales'] for item in sales_by_region}

    # def get_sales_by_time_of_year(self):
    #     # Query the database to get sales data by month
    #     sales_by_month = {}
    #     for month in range(1, 13):
    #         month_sales = Sale.objects.filter(
    #             created_at__month=month
    #         ).aggregate(revenue=Sum(F('quantity') * F('price')))['revenue']
    #         sales_by_month[datetime(2023, month, 1).strftime('%B')] = month_sales or 0
    #     return sales_by_month
    

