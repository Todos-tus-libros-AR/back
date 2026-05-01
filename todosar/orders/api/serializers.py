from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from ..models import Order, OrderItem, Discount


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["ean", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["id", "items", "book_store_id", "total"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        total = sum(item["quantity"] * item["unit_price"] for item in items_data)
        order = Order.objects.create(**validated_data, total=total)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order


class DiscountSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    left_uses = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ["code", "type", "value", "expiration", "max_uses", "left_uses"]

    @extend_schema_field(serializers.IntegerField())
    def get_value(self, obj):
        if obj.type == "percentage":
            return obj.percentage
        return obj.fixed

    @extend_schema_field(serializers.IntegerField())
    def get_left_uses(self, obj):
        return obj.max_uses - obj.current_uses
