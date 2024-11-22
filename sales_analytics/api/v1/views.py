from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SalesPerformanceSerializer
from sales_analytics.services import SalesPerformanceService

class SalesPerformanceView(APIView):
    def get(self, request):
        print("SalesPerformanceView.get() called!")
        service = SalesPerformanceService()
        revenue_trends = service.get_revenue_trends()
        sales_by_product = service.get_sales_by_product()
        sales_by_region = service.get_sales_by_region()
        sales_by_time_of_year = service.get_sales_by_time_of_year()
        data = {
            'revenue_trends': revenue_trends,
            'sales_by_product': sales_by_product,
            'sales_by_region': sales_by_region,
            'sales_by_time_of_year': sales_by_time_of_year
        }
        serializer = SalesPerformanceSerializer(data)
        return Response(serializer.data)