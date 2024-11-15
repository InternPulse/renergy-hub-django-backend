from rest_framework import serializers

class SalesPerformanceSerializer(serializers.Serializer):
    revenue_trends = serializers.DictField()
    sales_by_product = serializers.DictField()
    # sales_by_region = serializers.DictField()
    # sales_by_time_of_year = serializers.DictField()