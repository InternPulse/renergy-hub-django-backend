from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import Counter
from .api_client  import ProductManagementAPI
from .serializers import ResponseSerializer

class TopSellingProductsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            api_client = ProductManagementAPI()
            products = api_client.get_products()

            product_names = [product['name'] for product in products]
            name_counts = Counter(product_names)
            top_selling_products = [{"name": name, "count": count} for name, count in name_counts.most_common()]

            serializer = ResponseSerializer(data={"data": top_selling_products})
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
