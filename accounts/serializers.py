from typing import Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as OriginTokenObtainPairSerializer,
    TokenRefreshSerializer as OriginTokenRefreshSerializer,
)
from books.serializers import ApplicationsSerializer

User = get_user_model()


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2", "gender", "position", "birthdate", "phone_num"]
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['phone_num'],
                message="이미 가입된 휴대폰 번호입니다."
            )
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Difference between passwords")
        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]
        phone_num = validated_data["phone_num"]
        gender = validated_data.get("gender", "")
        position = validated_data.get("position", "")
        birthdate = validated_data.get("birthdate", None)

        new_user = User(email=email, username=username, gender=gender, position=position, birthdate=birthdate, phone_num=phone_num)
        new_user.set_password(password)
        new_user.save()

        return new_user


class TokenObtainPairSerializer(OriginTokenObtainPairSerializer):
    def validate(self, attrs):
        data: Dict = super().validate(attrs)
        data["email"] = self.user.email
        data["is_staff"] = self.user.is_staff
        data["username"] = self.user.username

        return data


class TokenRefreshSerializer(OriginTokenRefreshSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    applications_set = ApplicationsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["email", "is_superuser",
                  "is_staff", "username",
                  "phone_num", "applications_set"]