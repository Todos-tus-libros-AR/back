from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from ..models import Order, OrderItem, Discount


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["ean", "amount"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items", "library"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order


class DiscountSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_value(self, obj):
        if obj.type == "percentage":
            return obj.percentage
        return obj.fixed

    left_uses = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_left_uses(self, obj):
        return obj.max_uses - obj.current_uses

    class Meta:
        model = Discount
        fields = ["code", "type", "value", "exp", "max_uses", "left_uses"]
