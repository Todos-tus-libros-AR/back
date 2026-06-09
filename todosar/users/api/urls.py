from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import UserAccessAPIView, UserAddressAPIView, UserMeAPIView, api_login

urlpatterns = [
    path("login/", api_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserAccessAPIView.as_view(), name="register"),
    path("user/me/", UserMeAPIView.as_view(), name="user-me"),
    
    path(
        "user/address/",
        UserAddressAPIView.as_view({"get": "list", "post": "create"}),
        name="user-addresses-list",
    ),
    
    path(
        "user/address/<int:pk>/",
        UserAddressAPIView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="user-addresses-detail",
    ),
]