from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Sum, Count
from .models import Product, SalesRecord, ProductEngagement
from .serializers import ProductSerializer
import logging

# Configure logging for debugging
logger = logging.getLogger(__name__)

# Custom Pagination Class
class CustomPagination(PageNumberPagination):
    page_size = 10


class TopSellingProductsView(APIView):
    def get(self, request):
        try:
            # Aggregate top-selling products
            top_products = (
                SalesRecord.objects
                .values('product')
                .annotate(total_sold=Sum('quantity'))
                .order_by('-total_sold')[:20]
            )

            products = Product.objects.filter(id__in=[item['product'] for item in top_products])

            # Paginate and serialize the results
            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(paginated_products, many=True)

            return paginator.get_paginated_response(serializer.data)  # Default: 200 OK
        except Exception as e:
            logger.error(f"Unexpected error in TopSellingProductsView: {e}")
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductEngagementView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        engagement_type = request.data.get('engagement_type')

        if not product_id or not engagement_type:
            return Response({'error': 'Product ID and Engagement Type are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)


        if engagement_type not in ['view', 'click']:
            return Response({'error': 'Invalid engagement type. Accepted values: "view", "click".'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ProductEngagement.objects.create(product=product, engagement_type=engagement_type)
            return Response({'message': 'Engagement recorded successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Unexpected error in ProductEngagementView POST: {e}")
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            # Aggregate engagement data
            engagement_data = (
                ProductEngagement.objects
                .select_related('product')
                .values('product__name')
                .annotate(total_engagements=Count('id'))
                .order_by('-total_engagements')
            )

            # Paginate and format the response
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(engagement_data, request)
            response_data = [
                {
                    'product_name': item['product__name'],
                    'total_engagements': item['total_engagements']
                } for item in paginated_data
            ]

            return paginator.get_paginated_response(response_data)  # Default: 200 OK
        except Exception as e:
            logger.error(f"Unexpected error in ProductEngagementView GET: {e}")
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProfitMarginView(APIView):
    def get(self, request):
        try:
            # Fetch all products
            products = Product.objects.all()
            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(products, request)

            # Calculate profit margin for each product
            profit_margins = [
                {
                    'product_name': product.name,
                    'profit_margin': round((product.selling_price - product.cost_price) / product.selling_price * 100, 2)
                    if product.selling_price > 0 else 0
                } for product in paginated_products
            ]

            return paginator.get_paginated_response(profit_margins)  # Default: 200 OK
        except ZeroDivisionError:
            return Response({'error': 'Division by zero occurred while calculating profit margin.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in ProfitMarginView: {e}")
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
