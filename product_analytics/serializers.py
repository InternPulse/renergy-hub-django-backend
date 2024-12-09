from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    count = serializers.IntegerField()

class ResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default="success")
    message = serializers.CharField(default="Data retrieved successfully")
    data = ProductSerializer(many=True)
