from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Renergy Hub Django Backend API. Please use /api/v1/ to access the API endpoints.")

urlpatterns = [
    path('', home, name='home'),  # Add this line to handle the root URL
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('financial/', include('financial_analytics.urls')),
        path('marketing/', include('marketing_analytics.urls')),
        path('sales/', include('sales_analytics.urls')),
        path('product/', include('product_analytics.urls')),
    ])),
    path('Api/v1/', RedirectView.as_view(url='/api/v1/', permanent=True)),  # Redirect uppercase to lowercase
]