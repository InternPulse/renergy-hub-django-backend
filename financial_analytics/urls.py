from django.urls import path, include
from financial_analytics.routers import router

urlpatterns = [
    path('', include(router.urls)), 
]




