from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.db.models import Q, F

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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: DiscountSerializer},
)
class DiscountListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        discounts = Discount.objects.filter(Q(user=request.user) | Q(user=None)).filter(
            current_uses__lt=F("max_uses")
        )
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
