from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.db.models import Q, F
from django.utils import timezone
import requests

from ..models import Discount

from .serializers import OrderSerializer, DiscountSerializer


@extend_schema(
    request=OrderSerializer,
    responses={201: OrderSerializer},
)
class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            items = validated_data.get("items", [])

            payload = {
                "nombre": request.user.first_name,
                "apellido": request.user.last_name,
                "email": request.user.email,
                "libreria": validated_data["book_store"],
                "descuento": 0,
                "productos": [
                    {"ean": item["ean"], "cantidad": item["quantity"]} for item in items
                ],
            }

            try:
                response = requests.post(
                    "https://apiultragestion.com.ar/api/external/generar-orden/",
                    headers={
                        "Authorization": "Token a2f8b8e03a87be5a6dcf54ed588b4e04303b70ee"
                    },
                    json=payload,
                )
                if response.status_code not in [200, 201]:
                    return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(
                    {"error": "No se pudo conectar al sistema externo"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            external_data = response.json()
            order = serializer.save(
                user=request.user,
                order_link=external_data.get("order_link"),
                order_id=str(external_data.get("order_id")),
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: DiscountSerializer},
)
class DiscountListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        discounts = (
            Discount.objects.filter(Q(user=request.user) | Q(user=None))
            .filter(current_uses__lt=F("max_uses"))
            .filter(Q(expiration__gt=timezone.now()) | Q(expiration=None))
        )
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
