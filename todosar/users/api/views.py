import os
from django.conf import settings
from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from utils.email import Emailing
from utils.models import GeneralConfiguration

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

            general_config = GeneralConfiguration.load()

            if getattr(general_config, "send_new_users_discount_email", False):
                emailing.send_discount_for_new_users(user.email, user)
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


User = get_user_model()

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        
        if not email:
            return Response({"detail": "El email es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            scheme = request.is_secure() and "https" or "http"
            origin = request.headers.get('Origin')
            
            frontend_url = origin or getattr(settings, "FRONTEND_URL")
            reset_link = f"{frontend_url}/recuperar-password?uid={uid}&token={token}"
            
            emailing = Emailing()
            emailing.send_password_reset(user.email, reset_link)
            
            return Response(
                {"detail": "Si el correo está registrado, recibirás un enlace de recuperación."}, 
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {"detail": "Si el correo está registrado, recibirás un enlace de recuperación."}, 
                status=status.HTTP_200_OK
            )

class PasswordResetValidateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Response({"detail": "Token válido."}, status=status.HTTP_200_OK)
        return Response({"detail": "Enlace inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"detail": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
            
        return Response({"detail": "Enlace inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)