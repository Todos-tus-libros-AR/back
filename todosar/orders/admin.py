from django.contrib import admin
from .models import Order, OrderItem, Discount


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "book_store",
        "total_amount",
        "status",
        "order_id",
        "order_link",
        "order_token",
        "created",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "ean", "quantity", "unit_price")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "type", "expiration")
