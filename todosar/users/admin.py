from django.contrib import admin

from .models import User, UserAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "birth_date")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "street",
        "number",
        "door",
        "postal_code",
        "city",
        "state",
        "country",
        "main",
    )
    search_fields = (
        "user__username",
        "street",
        "number",
        "door",
        "postal_code",
        "city__name",
        "state__name",
        "country__name",
    )
