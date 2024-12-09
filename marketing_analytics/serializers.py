from rest_framework import serializers

class CartAbandonmentRateSerializer(serializers.Serializer):
    total_carts = serializers.IntegerField()
    purchased_carts = serializers.IntegerField()
    abandoned_carts = serializers.IntegerField()
    abandonment_rate = serializers.FloatField()
