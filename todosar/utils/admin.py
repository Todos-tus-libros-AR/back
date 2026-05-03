from django.contrib import admin

from .models import Country, GeneralConfiguration, State, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "ultra_code")
    search_fields = ("name", "ultra_code")


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "ultra_code", "country")
    search_fields = ("name", "ultra_code", "country__name")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "ultra_code", "state", "country")
    search_fields = ("name", "ultra_code", "state__name", "state__country__name")

    @admin.display(description="Country")
    def country(self, obj):
        return obj.state.country.name


@admin.register(GeneralConfiguration)
class GeneralConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "send_new_users_discount_email",
        "new_users_discount_percentage",
        "new_users_fixed_discount_amount",
    )
