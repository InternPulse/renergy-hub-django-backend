from rest_framework import routers
from .viewsets import FinancialAnalyticsViewSet

app_name = "financial_analytics"

router = routers.DefaultRouter()
router.register(r'analytics', FinancialAnalyticsViewSet, basename='financial-analytics') 









