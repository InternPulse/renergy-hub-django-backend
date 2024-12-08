from rest_framework import serializers

class SalesPerformanceSerializer(serializers.Serializer):
    status = serializers.CharField(default="success")
    message = serializers.CharField(default="Data retrieved successfully")
    revenue_trends = serializers.DictField()
    sales_by_product = serializers.DictField()
    # sales_by_region = serializers.DictField()
    sales_by_time_of_year = serializers.DictField()


