from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import csrf, CountryViewSet, StateViewSet, CityViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'states', StateViewSet, basename='state')
router.register(r'cities', CityViewSet, basename='city')

urlpatterns = [
    path("csrf/", csrf, name="csrf"),
    path("", include(router.urls)), 
]