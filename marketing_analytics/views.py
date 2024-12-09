from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import calculate_cart_abandonment_rate
from .serializers import CartAbandonmentRateSerializer

class CartAbandonmentRateAPIView(APIView):
    def get(self, request):
        stats = calculate_cart_abandonment_rate()
        serializer = CartAbandonmentRateSerializer(stats)
        return Response(serializer.data)

