from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as OriginTokenObtainPairSerializer,
    TokenRefreshSerializer as OriginTokenRefreshSerializer,
)

User = get_user_model()


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2", "gender", "position", "birthdate", "phone_num"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Difference between passwords")
        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]
        phone_num = validated_data["phone_num"]
        gender = validated_data.get("gender", None)
        position = validated_data.get("position", None)
        birthdate = validated_data.get("birthdate", "1970-01-01")

        new_user = User(email=email, username=username, gender=gender, position=position, birthdate=birthdate, phone_num=phone_num)
        new_user.set_password(password)
        new_user.save()

        return new_user


class TokenObtainPairSerializer(OriginTokenObtainPairSerializer):
    def validate(self, attrs):
        data: Dict = super().validate(attrs)
        data["email"] = self.user.email
        data["is_staff"] = self.user.is_staff

        return data


class TokenRefreshSerializer(OriginTokenRefreshSerializer):
    pass
