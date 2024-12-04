from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    categoryName = serializers.CharField()
    description = serializers.CharField()

class ProductAnalyticsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    image = serializers.URLField()
    created_at = serializers.DateTimeField()
    total_revenue = serializers.FloatField()
    total_cost = serializers.FloatField()
    total_quantity_sold = serializers.IntegerField()
    total_profit = serializers.FloatField()
    average_stock = serializers.FloatField()
    sales_data = serializers.ListField(child=serializers.DictField())
    
    # Additional analytics fields
    profit_margin = serializers.FloatField()
    average_price = serializers.FloatField()
    stock_turnover_rate = serializers.FloatField()
    is_profitable = serializers.BooleanField()
    profit_per_unit = serializers.FloatField()

