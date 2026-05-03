from django.urls import path

from .views import OrderCreateView, DiscountListView

urlpatterns = [
    path("order/", OrderCreateView.as_view(), name="order"),
    path("discounts/", DiscountListView.as_view(), name="discounts"),
]
