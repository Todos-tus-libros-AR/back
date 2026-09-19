from django.urls import path

from .views import OrderCreateView, DiscountListView, TNCallbackView

urlpatterns = [
    path("order/", OrderCreateView.as_view(), name="order"),
    path("discounts/", DiscountListView.as_view(), name="discounts"),
    path("tn-callbacks/", TNCallbackView.as_view(), name="TNCallback"),
]
