from django.urls import path
from .views import (
    FinancialAnalyticsView,
    TopProfitProductsView,
    LossMakingProductsView,
    ProfitMakingProductsView
)

urlpatterns = [
    path('analytics/', FinancialAnalyticsView.as_view(), name='financial-analytics'),
    path('analytics/top-profit/', TopProfitProductsView.as_view(), name='top-profit-products'),
    path('analytics/loss-making/', LossMakingProductsView.as_view(), name='loss-making-products'),
    path('analytics/profit-making/', ProfitMakingProductsView.as_view(), name='profit-making-products'),
    
]



