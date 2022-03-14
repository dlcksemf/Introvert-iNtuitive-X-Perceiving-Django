from collections import Counter
from datetime import timedelta, date
from typing import Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as OriginTokenObtainPairSerializer,
    TokenRefreshSerializer as OriginTokenRefreshSerializer,
)

from books.models import LoanedBooks
from books.serializers import LoanedBooksSerializer, ApplicationsSerializer, WishesSerializer

User = get_user_model()


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["user_id", "email", "username", "password", "password2", "gender", "position", "birthdate", "phone_num"]
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
        data["user_id"] = self.user.user_id
        data["is_staff"] = self.user.is_staff
        data["username"] = self.user.username

        return data


class TokenRefreshSerializer(OriginTokenRefreshSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    applications_set = ApplicationsSerializer(many=True, read_only=True)
    loanedbooks_set = LoanedBooksSerializer(many=True, read_only=True)
    wishes_set = WishesSerializer(many=True, read_only=True)
    count_loans = serializers.SerializerMethodField()
    loaned_dates = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["user_id", "applications_set", "loanedbooks_set", "wishes_set",
                  "is_staff", "email", "username", "phone_num", "gender",
                  "birthdate", "position", "created_at", "updated_at",
                  "count_loans", "loaned_dates","department","point"]

    def get_count_loans(self, instance):
        return instance.loanedbooks_set.count()

    def get_loaned_dates(self, instance):
        def date_range(start, end):
            delta = end - start
            days = [start + timedelta(days=i) for i in range(delta.days + 1)]
            return days

        try:
            loaned_dates = LoanedBooks.objects.all().filter(user_id=instance.user_id)
        except LoanedBooks.DoesNotExist:
            loaned_dates = []

        dates = Counter()

        if loaned_dates:
            for loandate in loaned_dates:
                if loandate.returned_date:
                    return_date = loandate.returned_date
                else:
                    return_date = date.today()

                dates.update(str(rkskek) for rkskek in date_range(loandate.loaned_date, return_date))

        return [ { 'day': key, 'value': value } for (key, value) in dates.items()]
