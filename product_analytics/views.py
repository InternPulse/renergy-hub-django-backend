from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from .models import Product, SalesRecord, ProductEngagement
from .serializers import ProductSerializer
from .pagination import CustomPagination  # Updated import

# Create your views here

class TopSellingProductsView(APIView):
    def get(self, request):
        try:
            top_products = (
                SalesRecord.objects
                .values('product')
                .annotate(total_sold=Sum('quantity'))
                .order_by('-total_sold')[:20]
            )

            products = Product.objects.filter(id__in=[item['product'] for item in top_products])

            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(paginated_products, many=True)

            return paginator.get_paginated_response(serializer.data)
        except Exception:
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
        except Exception:
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            engagement_data = (
                ProductEngagement.objects
                .select_related('product')
                .values('product__name')
                .annotate(total_engagements=Count('id'))
                .order_by('-total_engagements')
            )

            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(engagement_data, request)
            response_data = [
                {'product_name': item['product__name'], 'total_engagements': item['total_engagements']}
                for item in paginated_data
            ]

            return paginator.get_paginated_response(response_data)
        except Exception:
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfitMarginView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(products, request)

            profit_margins = [
                {
                    'product_name': product.name,
                    'profit_margin': round((product.selling_price - product.cost_price) / product.selling_price * 100, 2)
                    if product.selling_price > 0 else 0
                } for product in paginated_products
            ]

            return paginator.get_paginated_response(profit_margins)
        except ZeroDivisionError:
            return Response({'error': 'Division by zero occurred while calculating profit margin.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
