from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.db import transaction
from ..models import Order, OrderItem, Discount


class OrderItemSerializer(serializers.ModelSerializer):
    item_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["ean", "quantity", "unit_price", "item_amount"]

    @extend_schema_field(serializers.DecimalField(max_digits=12, decimal_places=2))
    def get_item_amount(self, obj):
        item_amount = obj.quantity * obj.unit_price
        return item_amount


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            "id",
            "items",
            "book_store",
            "total_amount",
            "status",
            "order_link",
            "order_id",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop("items")
            total_amount = sum(
                item["quantity"] * item["unit_price"] for item in items_data
            )
            order = Order.objects.create(**validated_data, total_amount=total_amount)
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
