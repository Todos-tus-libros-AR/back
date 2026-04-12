from django.contrib import admin

from .models import Country, State, City


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
