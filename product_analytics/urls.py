from django.urls import path
from .views import TopSellingProductsView, ProductEngagementView, ProfitMarginView

app_name = 'products'  # Namespacing the app

urlpatterns = [
    path('top-selling/', TopSellingProductsView.as_view(), name='top-selling'),
    path('engagement/', ProductEngagementView.as_view(), name='engagement'),
    path('profit-margin/', ProfitMarginView.as_view(), name='profit-margin'),
]
