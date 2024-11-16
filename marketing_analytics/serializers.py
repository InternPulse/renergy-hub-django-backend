from rest_framework import serializers

class CartAbandonmentRateSerializer(serializers.Serializer):
    abandonment_rate = serializers.FloatField()
