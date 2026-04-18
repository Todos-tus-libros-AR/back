from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets

from utils.email import Emailing

from ..models import UserAddress

from .serializers import UserAddressSerializer, UserCreationSerializer, UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)
    if not user:
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    login(request, user)
    return Response({"detail": "Login successful"})


@extend_schema(
    request=UserCreationSerializer,
    responses={201: UserCreationSerializer},
)
class UserAccessAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            emailing = Emailing()
            emailing.send_bienvenida(user.email)
            return Response(
                {"detail": "User created successfully", "user": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserSerializer,
    responses={200: UserSerializer},
)
class UserMeAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressAPIView(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
