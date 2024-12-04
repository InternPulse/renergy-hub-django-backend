from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api_client import ProductManagementAPI
from .pagination import CustomPageNumberPagination
from .serializers import ProductAnalyticsSerializer
from .product_analytics import ProductAnalytics

class BaseAnalyticsView(APIView):
    pagination_class = CustomPageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_api = ProductManagementAPI()
        self.product_analytics = ProductAnalytics()

    def paginate_results(self, request, product_analytics):
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(product_analytics, request)
        if page is not None:
            serializer = ProductAnalyticsSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProductAnalyticsSerializer(product_analytics, many=True)
        return Response(serializer.data)

    def handle_request(self, request):
        try:
            products = self.product_api.get_products()
            filtered_products = self.product_analytics.filter_products_by_date(products, **request.query_params)
            return filtered_products
        except ValueError as e:
            if "Invalid month" in str(e) or "Invalid day" in str(e):
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class FinancialAnalyticsView(BaseAnalyticsView):
    def get(self, request):
        filtered_products = self.handle_request(request)
        if isinstance(filtered_products, Response):
            return filtered_products

        product_analytics = self.product_analytics.calculate_product_analytics(filtered_products)

        min_profit = request.query_params.get('min_profit')
        if min_profit:
            product_analytics = [p for p in product_analytics if p['total_profit'] >= float(min_profit)]

        profitable_only = request.query_params.get('profitable_only')
        if profitable_only and profitable_only.lower() == 'true':
            product_analytics = [p for p in product_analytics if p['is_profitable']]

        return self.paginate_results(request, product_analytics)

class TopProfitProductsView(BaseAnalyticsView):
    def get(self, request):
        filtered_products = self.handle_request(request)
        if isinstance(filtered_products, Response):
            return filtered_products

        top_profit = self.product_analytics.get_top_profit_products(filtered_products)
        return self.paginate_results(request, top_profit)

class LossMakingProductsView(BaseAnalyticsView):
    def get(self, request):
        filtered_products = self.handle_request(request)
        if isinstance(filtered_products, Response):
            return filtered_products

        loss_making = self.product_analytics.get_loss_making_products(filtered_products)
        if not loss_making:
            return Response({"message": "No products are currently selling at a loss."}, status=status.HTTP_200_OK)
        return self.paginate_results(request, loss_making)

class ProfitMakingProductsView(BaseAnalyticsView):
    def get(self, request):
        filtered_products = self.handle_request(request)
        if isinstance(filtered_products, Response):
            return filtered_products

        profit_making = self.product_analytics.get_profit_making_products(filtered_products)
        return self.paginate_results(request, profit_making)