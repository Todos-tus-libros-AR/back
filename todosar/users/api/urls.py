from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import UserAccessAPIView, UserAddressAPIView, UserMeAPIView, api_login, PasswordResetRequestAPIView, PasswordResetValidateAPIView, PasswordResetConfirmAPIView

urlpatterns = [
    path("login/", api_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserAccessAPIView.as_view(), name="register"),
    path("user/me/", UserMeAPIView.as_view(), name="user-me"),
    path("password_reset/", PasswordResetRequestAPIView.as_view(), name="password-reset"),
    path("password_reset/validate_token/", PasswordResetValidateAPIView.as_view(), name="password-reset-validate"),
    path("password_reset_confirm/", PasswordResetConfirmAPIView.as_view(), name="password-reset-confirm"),
    path(
        "user/address/",
        UserAddressAPIView.as_view({"get": "list", "post": "create"}),
        name="user-addresses-list",
    ),
    path(
        "user/address/<int:pk>/",
        UserAddressAPIView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="user-addresses-detail",
    ),
    path(
        r"password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
