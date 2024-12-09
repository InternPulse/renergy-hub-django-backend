from django.urls import path
from .views import TopSellingProductsView

urlpatterns = [
    path('top-selling/', TopSellingProductsView.as_view(), name='top-selling'),
]