from django.contrib import admin
from django.urls import path, include

api_url_patterns = [
    path('sales/', include('sales_analytics.urls')),
    path('product/', include('product_analytics.urls')),
    path('marketing/', include('marketing_analytics.urls')),
    path('financial/', include('financial_analytics.urls')),
]



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1', include(api_url_patterns)),  # Base API path
]