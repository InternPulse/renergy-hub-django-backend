from rest_framework import serializers

class SalesPerformanceSerializer(serializers.Serializer):
    status = serializers.CharField(default="success")
    message = serializers.CharField(default="Data retrieved successfully")
    data = serializers.DictField()