from django.urls import path
from .views import CartAbandonmentRateAPIView

urlpatterns = [
    path('api/v1/cart-abandonment-rate/', CartAbandonmentRateAPIView.as_view(), name='api_cart_abandonment_rate'),
]


