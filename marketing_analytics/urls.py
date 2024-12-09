from django.urls import path
from .views import CartAbandonmentRateAPIView

urlpatterns = [
    path('abandonment-rate', CartAbandonmentRateAPIView.as_view(), name='abandonment_rate'),
    path('abandonment-rate/', CartAbandonmentRateAPIView.as_view(), name='abandonment_rate_slash'),
]