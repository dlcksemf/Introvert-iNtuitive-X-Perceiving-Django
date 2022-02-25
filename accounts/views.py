from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView as OriginTokenObtainPairView,
    TokenRefreshView as OriginTokenRefreshView,
)
from accounts.serializers import TokenObtainPairSerializer, UserCreationSerializer, UserSerializer
from books.paginations.BookApplicationsPagination import BookApplicationPagination

User = get_user_model()


class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = [AllowAny]


class TokenObtainPairView(OriginTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(OriginTokenRefreshView):
    pass


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = BookApplicationPagination

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(username__icontains=query)
        if query:
            qs = qs.filter(conditions)

        return qs

#
# class UserDetail(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
