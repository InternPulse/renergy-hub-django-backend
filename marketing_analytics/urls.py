from django.urls import path
from .views import CartAbandonmentRateAPIView

urlpatterns = [
    path("", CartAbandonmentRateAPIView.as_view(), name="api_cart_abandonment_rate"),
]
