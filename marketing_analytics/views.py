from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import calculate_cart_abandonment_rate
from .serializers import CartAbandonmentRateSerializer







class CartAbandonmentRateAPIView(APIView):
    def get(self, request):
        # Calculate stats
        stats = calculate_cart_abandonment_rate()
        # Serialize data
        serializer = CartAbandonmentRateSerializer(stats)
        return Response(serializer.data)
