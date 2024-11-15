from django.contrib import admin
from django.urls import path, include
from .api.v1 import views

urlpatterns = [
    path('', views.SalesPerformanceView.as_view(), name='sales-performance'),
]