from rest_framework import viewsets, permissions
from .serializers import CountrySerializer, StateSerializer, CitySerializer
from utils.models import Country, State, City

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

class StateViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = State.objects.all()
        country_id = self.request.query_params.get('country')
        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
        return queryset

class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = City.objects.all()
        state_id = self.request.query_params.get('state')
        if state_id is not None:
            queryset = queryset.filter(state_id=state_id)
        return queryset