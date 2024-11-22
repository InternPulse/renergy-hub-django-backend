# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_cart_abandonment_rate
from .serializers import CartAbandonmentRateSerializer

class CartAbandonmentRateAPIView(APIView):
    """
    API endpoint to get the cart abandonment rate.
    """
    def get(self, request, *args, **kwargs):
        abandonment_rate = get_cart_abandonment_rate()
        serializer = CartAbandonmentRateSerializer({'abandonment_rate': abandonment_rate})
        return Response(serializer.data, status=status.HTTP_200_OK)
