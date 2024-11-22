from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils import generate_mock_product_data
from datetime import datetime
from collections import defaultdict
import calendar
from .permissions import IsVendor
from rest_framework.permissions import IsAuthenticated



class FinancialAnalyticsViewSet(viewsets.ViewSet):
    # Temporarily remove permission for development/testing
    # permission_classes = [IsAuthenticated, IsVendor]  # Only authenticated Vendors have access

    """
    Viewset for calculating and displaying financial analytics.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products = generate_mock_product_data(num_products=10, years=3)

    def list(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        day = request.query_params.get('day')
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        date = request.query_params.get('date')

        try:
            if month:
                if not 1 <= int(month) <= 12:
                    return Response({"message": "Invalid month. Month must be between 1 and 12."}, status=status.HTTP_400_BAD_REQUEST)
            
            if day:
                if not 1 <= int(day) <= 31:
                    return Response({"message": "Invalid day. Day must be between 1 and 31."}, status=status.HTTP_400_BAD_REQUEST)

            filtered_products = self.filter_products_by_date(self.products, start_date, end_date, day, month, year, date)

            if not filtered_products:
                return Response({"message": "No records found for the specified date range."}, status=status.HTTP_404_NOT_FOUND)

            product_analytics = self.calculate_product_analytics(filtered_products)

            return Response({
                "message": "Records retrieved successfully.",
                "products": list(product_analytics.values())
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def top_products(self, request):
        products = list(self.calculate_product_metrics().values())
        sorted_products = sorted(products, key=lambda x: x['total_profit'], reverse=True)
        top_5 = sorted_products[:5]

        return Response({
            "message": "Top 5 products by profit retrieved successfully.",
            "top_products": top_5
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def selling_at_loss(self, request):
        products = list(self.calculate_product_metrics().values())
        loss_products = [p for p in products if p['total_profit'] < 0]
        sorted_loss_products = sorted(loss_products, key=lambda x: x['total_profit'])

        if not loss_products:
            return Response({
                "message": "No products are currently selling at a loss.",
                "loss_products": []
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Products selling at a loss retrieved successfully.",
            "loss_products": sorted_loss_products
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def profit_records(self, request):
        products = list(self.calculate_product_metrics().values())
        profit_products = [p for p in products if p['total_profit'] > 0]
        sorted_profit_products = sorted(profit_products, key=lambda x: x['total_profit'], reverse=True)

        if not profit_products:
            return Response({
                "message": "No products are currently making a profit.",
                "profit_products": []
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Profit records retrieved successfully.",
            "profit_products": sorted_profit_products
        }, status=status.HTTP_200_OK)

    def filter_products_by_date(self, products, start_date, end_date, day, month, year, date):
        try:
            if start_date and end_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                return [p for p in products if start.date() <= p['sale_date'].date() <= end.date()]
            elif date:
                target_date = datetime.strptime(date, "%Y-%m-%d")
                return [p for p in products if p['sale_date'].date() == target_date.date()]
            elif day and month and year:
                return [p for p in products if p['sale_date'].day == int(day) and 
                                               p['sale_date'].month == int(month) and 
                                               p['sale_date'].year == int(year)]
            elif month and year:
                return [p for p in products if p['sale_date'].month == int(month) and 
                                               p['sale_date'].year == int(year)]
            elif month:
                return [p for p in products if p['sale_date'].month == int(month)]
            elif day:
                return [p for p in products if p['sale_date'].day == int(day)]
            elif year:
                return [p for p in products if p['sale_date'].year == int(year)]
            else:
                return products
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")

    def calculate_product_analytics(self, products):
        product_analytics = defaultdict(lambda: {
            "product_id": "",
            "category_id": "",
            "user_id": "",
            "name": "",
            "description": "",
            "image": "",
            "created_at": "",
            "total_revenue": 0,
            "total_cost": 0,
            "total_quantity_sold": 0,
            "total_profit": 0,
            "average_stock": 0,
            "sales_data": []
        })

        for product in products:
            p_id = product['product_id']
            product_analytics[p_id]['product_id'] = p_id
            product_analytics[p_id]['category_id'] = product['category_id']
            product_analytics[p_id]['user_id'] = product['user_id']
            product_analytics[p_id]['name'] = product['name']
            product_analytics[p_id]['description'] = product['description']
            product_analytics[p_id]['image'] = product['image']
            product_analytics[p_id]['created_at'] = product['created_at'].isoformat()
            product_analytics[p_id]['total_revenue'] += product['price'] * product['quantity_sold']
            product_analytics[p_id]['total_cost'] += product['cost_price'] * product['quantity_sold']
            product_analytics[p_id]['total_quantity_sold'] += product['quantity_sold']
            product_analytics[p_id]['average_stock'] += product['stock']
            product_analytics[p_id]['sales_data'].append({
                "date": product['sale_date'].isoformat(),
                "price": product['price'],
                "quantity_sold": product['quantity_sold'],
                "revenue": product['price'] * product['quantity_sold'],
                "cost": product['cost_price'] * product['quantity_sold'],
                "profit": (product['price'] - product['cost_price']) * product['quantity_sold']
            })

        for p_id, data in product_analytics.items():
            data['total_profit'] = data['total_revenue'] - data['total_cost']
            data['average_stock'] /= len([p for p in products if p['product_id'] == p_id])

        return product_analytics

    def calculate_product_metrics(self):
        return self.calculate_product_analytics(self.products)