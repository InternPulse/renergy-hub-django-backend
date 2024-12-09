from rest_framework import serializers

class CartAbandonmentRateSerializer(serializers.Serializer):
    abandonment_rate = serializers.FloatField(allow_null=True)
    total_carts = serializers.IntegerField()
    abandoned_carts = serializers.IntegerField()
    message = serializers.CharField(allow_null=True)