from django.contrib.auth.password_validation import validate_password

from utils.api.serializers import CitySerializer, CountrySerializer, StateSerializer
from ..models import User, UserAddress
from rest_framework import serializers


class UserCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"]
        return User.objects.create_user(**validated_data)


class UserAddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    city_id = serializers.IntegerField(write_only=True)
    state_id = serializers.IntegerField(write_only=True)
    country_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserAddress
        fields = [
            "id",
            "street",
            "number",
            "door",
            "postal_code",
            "city",         # Salida
            "state",        # Salida
            "country",      # Salida
            "city_id",      # Entrada
            "state_id",     # Entrada
            "country_id",   # Entrada
            "main",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        
        if validated_data.get("main", False):
            UserAddress.objects.filter(user=user, main=True).update(main=False)
            
        return UserAddress.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if validated_data.get("main", False):
            UserAddress.objects.filter(user=user, main=True).update(main=False)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    user_addresses = UserAddressSerializer(
        many=True, read_only=True, source="addresses"
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "birth_date", "user_addresses"]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
