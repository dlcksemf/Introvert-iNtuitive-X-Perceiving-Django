import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView as OriginTokenObtainPairView,
    TokenRefreshView as OriginTokenRefreshView,
)
from accounts.serializers import TokenObtainPairSerializer, UserCreationSerializer, UserSerializer
from accounts.models import User as member

User = get_user_model()


class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = [AllowAny]


class TokenObtainPairView(OriginTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(OriginTokenRefreshView):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = member.objects.all()
    serializer_class = UserSerializer


def User_List(request):
    qs = member.objects.all()
    data = [
        {
            "username": User.username,
            "email": User.email,
        }
        for User in qs
    ]
    json_string = json.dumps(data)
    return HttpResponse(json_string)


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
